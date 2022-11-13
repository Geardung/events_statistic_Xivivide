
from fastapi import APIRouter, Depends, status, Response
import repository.eventers
from fastapi.responses import PlainTextResponse


router = APIRouter(prefix='/eventers', tags=['Ивентёры'])



@router.get('/get_statistic_by_id', status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def get_statistic_by_id(eventer_id: int, start: str, end: str, password: str):
    """
    
    Подготавливает статистику на определённого ивентёра
    
    Аргументы запроса:
    
        eventer_id (число): ID ивентёра, на которого нужно сделать статистику
        
        start (строка): Дата в формате 30.12.22
        
        end (строка): Дата в формате 30.12.22
        
        password (str): Пароль короче твой, который ты получил у Тэдэши#2468
        
    """
    

    return repository.eventers.get_statistic_by_id(eventer_id=eventer_id, start=start, end=end, password=password)


@router.get('/get_statistic_all', status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def get_statistic_all(start: str, end: str, password: str):
    """
    
    Подготавливает статистику на всех ивентёров (и клозеров сорян хехп)
    
    Аргументы запроса:
    
        start (строка): Дата в формате 30.12.22
        
        end (строка): Дата в формате 30.12.22
        
        password (str): Пароль короче твой, который ты получил у Тэдэши#2468
        
    """
    

    return repository.eventers.get_statistic_all(start=start, end=end, password=password)


@router.get('/get_aver_ex_events', status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def get_aver_ex_events(password: str):
    """
    
    Подготавливает статистику на определённого ивентёра
    
    Аргументы запроса:
    
        password (str): Пароль короче твой, который ты получил у Тэдэши#2468
        
    """
    

    return repository.eventers.get_aver_ex_events(password=password)