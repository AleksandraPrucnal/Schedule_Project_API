class ScheduleValidationException(Exception):
    """
    Wyjątek dla walidacji harmonogramu.
    Integracja z dyspozycyjnością pracy. 
    Zastosowanie: 
        - błędnie przypisane godziny harmonogramu niezgodne z dyspozycyjnością
        - przypisanie kolejnego harmonogramu na ten sam dzień tej samej osobie 
    """
    pass
