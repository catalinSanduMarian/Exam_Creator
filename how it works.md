how it works:
----> selectie problema
--- adaug o intrebare in set/subet whatev
--- pt problema x, selectez subsetul din care sa creez pb


la deschiderea proj/programului:
    --- initializez qtypes din fisierul X


incarcare problema back-end:
    ---> pb_text
    ---> pb_variables
    ---> pb 
    ---> pb_type_name
    ---> pb_name
    --- generez pb_id
    --- adaug pb_id in typul corect
    --- creez un folder cu numele pb_name cu cele 2 fisiere value si input  

    trb sa am si metoda de adaugat tip nou care are copii si un parinte(eventual)

pentru fiecare varianta_examen
    pentru fiecare problema
    ----> adaugare probelma:
    --- aleg o pb din subsetul de pb corect -> done
    --- incarc problema din folderul ei, citind cele 2 fisiere aferente (fieserul text si fisierul values). -> done
    --- Aleg valori pt variabile -> done
    --- calculez functiile -> done
    --- 2 tipuri de variabile: hidden si normal -> default sunt normale -> done
    --- generez 2 examene (sau un examen si un aswer sheet?) si le printez pe ambele --- later












UI STUFF:


incarcare problema UI:
o sa am de facut un UI OKAY's. 
    - o casuta unde pun textul
    - o casuta unde adaug numele variabilelor si valorile lor posibile(o val, un interval sau o lista)
    +- o casuta pt fisierul latex
    - ceva pentru raspunsuri
    o casuta pt raspunsuri


