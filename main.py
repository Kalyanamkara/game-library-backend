from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from  passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime ,timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



SECRET_KEY= "A*@49KDBA)9829e"
ALGORITHM= "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



DATABASE_URL = "sqlite:///./oyunlar.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class  UserDB(Base):
    __tablename__ ="users"

    id= Column(Integer, primary_key=True, index=True)
    username=Column(String, unique=True, index=True)
    hashed_password = Column(String)


class OyunDB(Base):
    __tablename__ = "oyunlar"
    
    id = Column(Integer, primary_key=True, index=True) 
    isim = Column(String, index=True)
    tur = Column(String)
    puan = Column(Integer)
    yapımcı = Column(String)


Base.metadata.create_all(bind=engine)


class OyunSema(BaseModel):
    isim: str
    tur: str
    puan: int
    yapımcı: str


class OyunGuncelle(BaseModel):
    isim: str | None = None
    tur: str | None = None
    puan: int | None = None
    yapımcı: str | None  = None

app = FastAPI()


class UserCreate(BaseModel):
    username: str
    password: str

def sifrele(sifre: str):
    return pwd_context.hash(sifre)
def sifre_dogrula(duz_sifre, hashlenmis_sifre):
    return pwd_context.verify(duz_sifre,hashlenmis_sifre)

def token_olustur(data: dict):
    to_encode= data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


        
    
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user is None:
        raise credentials_exception
    return user





    


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Biletiniz geçersiz veya süresi dolmuş",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user= db.query(UserDB).filter(UserDB.username == username).first()

    if user is None:
        raise credentials_exception
    return user
@app.post("/token")
def giris_yap(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    kullanici =db.query(UserDB).filter(UserDB.username==form_data.username).first()

    if not kullanici or not sifre_dogrula(form_data.password,kullanici.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanici adi veya sifre hatali",
            headers= {"WWW-Authenticate":"Bearer"},

        )
    access_token= token_olustur(data={"sub":kullanici.username})
    return {"access_token": access_token, "token_type":"bearer"}

@app.post("/register")
def kayit_ol(kullanici:UserCreate, db: Session= Depends(get_db)):
    sifreli_sifre = sifrele(kullanici.password)

    yeni_kullanici =UserDB(username=kullanici.username, hashed_password=sifreli_sifre)
    db.add(yeni_kullanici)
    db.commit()
    db.refresh(yeni_kullanici)

    return{"Kullanici olusturuldu": yeni_kullanici.username}



@app.post("/oyun-ekle")
def oyun_ekle(oyun: OyunSema, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    
    yeni_oyun = OyunDB(isim=oyun.isim, tur=oyun.tur, puan=oyun.puan , yapımcı= oyun.yapımcı)
    db.add(yeni_oyun)  
    db.commit()        
    db.refresh(yeni_oyun)
    return yeni_oyun

@app.get("/oyunlar")
def oyunlari_getir(db: Session = Depends(get_db)):
    
    tum_oyunlar = db.query(OyunDB).all()
    return tum_oyunlar

@app.delete("/oyun-sil/{oyun_id}")
def oyun_sil(oyun_id: int, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    
    silinecek_oyun = db.query(OyunDB).filter(OyunDB.id == oyun_id).first()
    
    if silinecek_oyun is None:
        raise HTTPException(status_code=404, detail="Aga bu ID ile oyun bulunamadı!")
    
    db.delete(silinecek_oyun)
    db.commit() 
    return {"bilgi": "Oyun başarıyla silindi", "silinen_id": oyun_id}


@app.get("/ben-kimim")
def profilimi_goster(current_user: UserDB = Depends(get_current_user)):
    return {"kullanici_adi": current_user.username, "mesaj":  "Bu  mesajı sadece giriş yapanlar görebilir."}


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
    
    if guncel_veri.yapımcı is not None:
        kayitli_oyun.yapımcı =guncel_veri.yapımcı

    
    db.commit()
    db.refresh(kayitli_oyun)
    
    return {"mesaj": "Oyun başarıyla güncellendi", "yeni_hal": kayitli_oyun}