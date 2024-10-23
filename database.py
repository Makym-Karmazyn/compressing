from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import DeclarativeBase , sessionmaker, Mapped, mapped_column, relationship
from sqlalchemy import Table, Column ,create_engine , String, ForeignKey

engine = create_engine("sqlite:///hyffman.db", echo=True )
Session = sessionmaker(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    def create_db():
        Base.metadata.create_all(engine)

    def drop_db():
        Base.metadata.drop_all(engine)


class HuffmanCode(Base):
    __tablename__ = 'huffman_codes'
    id: Mapped[str] = mapped_column(INTEGER(), primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(), nullable=False)
    code: Mapped[str] = mapped_column(String(),nullable=False)
    password: Mapped[str] = mapped_column(String(),nullable=False)




# Base.drop_db()
# Base.create_db()
stage = 0

def check_password(password):
    pasword_dublicat = session.query(HuffmanCode).filter_by(password=password).first()
    if pasword_dublicat:
        return True
    else:
        return False


def save_code(codes, password):
    for symbol, code in codes.items():
        # Перевірка, чи символ вже існує в базі
        if stage == 1:
            existing_record = session.query(HuffmanCode).filter_by(symbol=symbol, password=password).first()
            if existing_record is None:  # Якщо символа ще немає в базі
                huffman_code = HuffmanCode(symbol=symbol, code=code, password=password)
                session.add(huffman_code)
        else:
                huffman_code = HuffmanCode(symbol=symbol, code=code, password=password)
                session.add(huffman_code)

    session.commit()  # Підтверджуємо зміни

def load_code(password):
    codes = {}
    all_codes = session.query(HuffmanCode).filter_by(password=password).all()

    for i in all_codes:
        codes[i.symbol] = i.code

    return codes