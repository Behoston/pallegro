# pyllegro

<img src="https://raw.github.com/Behoston/pyllegro/master/misc/logo.png"  height="200" width="200" title="pyllegro logo" />


<a href="http://allegro.pl" target="_blank">allegro</a> WEB and REST API for Python


## Cele
 - Udostępnienie wygodnego API w Pythonie do łączenia się z serwisem allegro
 - Ułatwienie późniejszej integracji w Django
 
## Założenia
 - Wszystkie dostępne metody API powinny zostać zaimplementowane
 - Kod musi być przetestowany (jak tylko allegro naprawi środowisko deweloperskie)
 - Kod musi zawierać prykłady użycia pozwalające na zrozumienie zachowania pyllegro (jak tylko allegro naprawi środowisko deweloperskie)
 - Dokumentacja powinna być zawarta w kodzie programu
 - Implementacja powinna zawierać zarówno `webapi` jak i `REST API` i umożliwiać korzystanie z obydwu w dość przezroczysty sposób
 - Wszelkie błędy i niedociągnięcia po stronie API powinny być wyraźnie zaznaczone w miejscu w którym problem występuje

## Jak to działa?
<img src="https://raw.github.com/Behoston/pyllegro/master/misc/diagram.png" title="diagram" />

Na pomarańczowo oznaczone są elementy obsługiwane po stronie serwisu allegro, kolorem niebieskim elementy pyllegro.<br>
Allegro udostępnia WebApi za pomocą WSDL, które jest bardzo przestarzałe 
(użytkownik jest zmuszony podawać hasło do konta, żeby można było zintegrować program z allegro) 
oraz REST API, które wspiera OAuth. Niestety REST API jest rozwijane bardzo powolnie i na dzień dzisiejszy dostępna jest tylko jedna metoda.
Po zalogowaniu do REST API (poprzez OAuth) jesteśmy w stanie zalogować się w bezpieczny sposób do WebApi i używać wszystkich dostępnych w nim metod.
