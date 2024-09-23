% Персонажи
character(vault_dweller).      % Обитатель Убежища
character(brotherhood_knight). % Рыцарь Братства Стали
character(raider).             % Рейдер
character(super_mutant).       % Супермутант
character(ghoul).              % Гуль
character(minuteman).          % Минитмен
character(dog).                % Собака
character(deathclaw).          % Коготь смерти

% Локации
location(vault_13).            % Убежище 13
location(brotherhood_bunker).  % Бункер Братства Стали
location(raider_camp).         % Лагерь Рейдеров
location(cathedral).           % Собор
location(necropolis).          % Некрополь
location(gas_station).         % Автозаправочная станция
location(village).             % Деревня
location(wasteland).           % Пустошь

% Оружие
weapon(laser_rifle).           % лазерное ружье
weapon(homemade_pistol).       % самодельный пистолет
weapon(minigun).               % пулемет
weapon(plasma_pistol).         % плазменный пистолет
weapon(melee_weapon).          % ближний бой
weapon(fat_man).               % Пусковая установка

% Локации, где находятся персонажи
located_at(vault_dweller, vault_13).
located_at(brotherhood_knight, brotherhood_bunker).
located_at(raider, raider_camp).
located_at(super_mutant, cathedral).
located_at(ghoul, necropolis).
located_at(dog, gas_station).
located_at(dog, village).
located_at(minuteman, village).
located_at(deathclaw, wasteland).

% Оружие, которое используют персонажи
uses_weapon(vault_dweller, plasma_pistol).
uses_weapon(brotherhood_knight, laser_rifle).
uses_weapon(raider, melee_weapon).
uses_weapon(super_mutant, minigun).
uses_weapon(ghoul, melee_weapon).
uses_weapon(dog, melee_weapon).
uses_weapon(minuteman, homemade_pistol).
uses_weapon(brotherhood_knight, fat_man).
uses_weapon(deathclaw, melee_weapon).

% Союзы и вражда
ally(vault_dweller, brotherhood_knight).
ally(vault_dweller, dog).
ally(raider, dog).
ally(brotherhood_knight, dog).

% vault_dweller
enemy(vault_dweller, raider).
enemy(vault_dweller, ghoul).
enemy(vault_dweller, super_mutant).
enemy(vault_dweller, deathclaw).

% raider
enemy(raider, vault_dweller).
enemy(raider, brotherhood_knight).
enemy(raider, ghoul).
enemy(raider, deathclaw).

% brotherhood_knight
enemy(brotherhood_knight, raider).
enemy(brotherhood_knight, super_mutant).
enemy(brotherhood_knight, ghoul).
enemy(brotherhood_knight, deathclaw).

% super_mutant
enemy(super_mutant, brotherhood_knight).
enemy(super_mutant, vault_dweller).
enemy(super_mutant, deathclaw).

% ghoul
enemy(ghoul, vault_dweller).
enemy(ghoul, raider).
enemy(ghoul, brotherhood_knight).
enemy(ghoul, deathclaw).

% deathclaw
enemy(deathclaw, vault_dweller).
enemy(deathclaw, raider).
enemy(deathclaw, brotherhood_knight).
enemy(deathclaw, dog).
enemy(deathclaw, super_mutant).
enemy(deathclaw, minuteman).
enemy(deathclaw, ghoul).

% Правило: если два персонажа враги, то они не могут быть союзниками
cannot_be_allies(X, Y) :- enemy(X, Y) ; enemy(Y, X).

% Правило: персонаж вооружен дальнобойным оружием, если он использует лазерное, плазменное или огнестрельное оружие
ranged_weapon(X) :- uses_weapon(X, plasma_pistol).
ranged_weapon(X) :- uses_weapon(X, laser_rifle).
ranged_weapon(X) :- uses_weapon(X, minigun).

% Правило: персонаж является угрозой для другого персонажа, если он вооружен дальнобойным оружием и является врагом для другого персонажа
threat(X, Y) :- X = deathclaw ; (enemy(X, Y), ranged_weapon(X)).

% Правило: персонаж очень опасен, если у него есть ядерное оружие толстяк
ultra_dangerous(X) :- uses_weapon(X, fat_man); X = deathclaw.

% Персонажи могут мирно сосуществовать, если они не враги и находятся в одной локации
peaceful_coexistence(X, Y) :- located_at(X, L), located_at(Y, L), \+ enemy(X, Y).

% Место безопасно для персонажа, если там нет его врагов
safe_location(X, L) :- located_at(X, L), \+ (located_at(Y, L), enemy(X, Y)).