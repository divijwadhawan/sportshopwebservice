from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Date, TIMESTAMP, select, func
from sqlalchemy.orm import declarative_base, Session, sessionmaker
import random

# Database configuration (modify with your actual credentials)
DB_URL = "postgresql://admin:ZaKcqToSzGQK7YCuBlNEeJT3mVOYG04D@dpg-d24dfveuk2gs73cfgmv0-a.frankfurt-postgres.render.com/sportsdb1"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Define ORM model
class FootballMatch(Base):
    __tablename__ = "football_matches"

    match_id = Column(Integer, primary_key=True, index=True)
    match_date = Column(Date)
    home_team = Column(String)
    away_team = Column(String)
    stadium = Column(String)
    city = Column(String)
    country = Column(String)
    home_score = Column(Integer)
    away_score = Column(Integer)
    competition = Column(String)
    season = Column(String)
    match_status = Column(String)
    attendance = Column(Integer)
    referee = Column(String)
    created_at = Column(TIMESTAMP)

# Initialize FastAPI app
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET all matches (limit optional)
@app.get("/matches/")
def get_matches(limit: int = 100):
    with Session(engine) as session:
        results = session.query(FootballMatch).limit(limit).all()
        return results

# GET match by ID
@app.get("/matches/{match_id}")
def get_match(match_id: int):
    with Session(engine) as session:
        match = session.query(FootballMatch).filter(FootballMatch.match_id == match_id).first()
        if match is None:
            raise HTTPException(status_code=404, detail="Match not found")
        return match

# GET random match
@app.get("/matches/random")
def get_random_match():
    with Session(engine) as session:
        match = session.execute(
            select(FootballMatch).order_by(func.random()).limit(1)
        ).scalar()
        return match
