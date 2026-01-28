from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


DATABASE_URL = "sqlite:///./oyunlar.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class OyunDB(Base):
    __tablename__ = "oyunlar"
    
    id = Column(Integer, primary_key=True, index=True) 
    isim = Column(String, index=True)
    tur = Column(String)
    puan = Column(Integer)


Base.metadata.create_all(bind=engine)


class OyunSema(BaseModel):
    isim: str
    tur: str
    puan: int


class OyunGuncelle(BaseModel):
    isim: str | None = None
    tur: str | None = None
    puan: int | None = None

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/oyun-ekle")
def oyun_ekle(oyun: OyunSema, db: Session = Depends(get_db)):
    
    yeni_oyun = OyunDB(isim=oyun.isim, tur=oyun.tur, puan=oyun.puan)
    db.add(yeni_oyun)  
    db.commit()        
    db.refresh(yeni_oyun)
    return yeni_oyun

@app.get("/oyunlar")
def oyunlari_getir(db: Session = Depends(get_db)):
    
    tum_oyunlar = db.query(OyunDB).all()
    return tum_oyunlar

@app.delete("/oyun-sil/{oyun_id}")
def oyun_sil(oyun_id: int, db: Session = Depends(get_db)):
    
    silinecek_oyun = db.query(OyunDB).filter(OyunDB.id == oyun_id).first()
    
    if silinecek_oyun is None:
        raise HTTPException(status_code=404, detail="Aga bu ID ile oyun bulunamadı!")
    
    db.delete(silinecek_oyun)
    db.commit() 
    return {"bilgi": "Oyun başarıyla silindi", "silinen_id": oyun_id}


@app.put("/oyun-guncelle/{oyun_id}")

@app.put("/oyun-guncelle/{oyun_id}")
def oyun_guncelle(oyun_id: int, guncel_veri: OyunGuncelle, db: Session = Depends(get_db)):
   
    kayitli_oyun = db.query(OyunDB).filter(OyunDB.id == oyun_id).first()

    if kayitli_oyun is None:
        raise HTTPException(status_code=404, detail="Aga oyun bulunamadı!")

    
    if guncel_veri.isim is not None:
        kayitli_oyun.isim = guncel_veri.isim
        
    
    if guncel_veri.tur is not None:
        kayitli_oyun.tur = guncel_veri.tur
        
    
    if guncel_veri.puan is not None:
        kayitli_oyun.puan = guncel_veri.puan

    
    db.commit()
    db.refresh(kayitli_oyun)
    
    return {"mesaj": "Oyun başarıyla güncellendi", "yeni_hal": kayitli_oyun}