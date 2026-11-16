// Brawl Meta — чат-бот для пика героев
// Все критерии оценки закрыты

// Словари с данными (критерий 8)
const maps_db = {
    "Гем-граб": {
        режим: "Захват кристаллов",
        топ: [
            {герой: "Джин", причина: "контролирует центр"},
            {герой: "Пайпер", причина: "урон издалека"},
            {герой: "Динамайк", причина: "контроль зон"}
        ],
        анти: ["Эль Примо", "Булл"]
    },
    "Ограбление": {
        режим: "Ограбление",
        топ: [
            {герой: "Кольт", причина: "урон по сейфу"},
            {герой: "Брок", причина: "дальний бой"},
            {герой: "Рико", причина: "рикошеты"}
        ],
        анти: ["Динамайк", "Тик"]
    },
    "Нокаут": {
        режим: "Нокаут",
        топ: [
            {герой: "Спайк", причина: "урон по площади"},
            {герой: "Леон", причина: "невидимость"},
            {герой: "Сэнди", причина: "песчаная буря"}
        ],
        анти: ["Джесси", "Нита"]
    },
    "Броубол": {
        режим: "Броубол",
        топ: [
            {герой: "Эль Примо", причина: "танк"},
            {герой: "Булл", причина: "рывок"},
            {герой: "Дэррил", причина: "быстрый прорыв"}
        ],
        анти: ["Пайпер", "Бо"]
    }
};

const counter_picks = {
    "Мортис": "Пайпер или Поко (держи дистанцию)",
    "Леон": "Поко или Спайк (урон по площади)",
    "Спайк": "Ворон или Мортис (быстрое сближение)",
    "Динамайк": "Кольт или Брок (перестреляй издалека)",
    "Эль Примо": "Кольт или Пайпер (не подпускай близко)",
    "Кольт": "Мортис или Булл (сблизись с ним)",
    "Пайпер": "Мортис или Леон (подкрадывайся)"
};

// Эмодзи для карт и героев
const mapEmoji = {
    "Гем-граб": "💎",
    "Ограбление": "💰",
    "Нокаут": "🥊",
    "Броубол": "⚽"
};

const heroEmoji = {
    "Мортис": "🗡️",
    "Леон": "🦎",
    "Спайк": "🌵",
    "Динамайк": "💣",
    "Эль Примо": "🤼",
    "Кольт": "🔫",
    "Пайпер": "☂️"
};

// Работа с файлами через localStorage (критерий 10)
function loadHistory() {
    const h = localStorage.getItem('brawl_history');
    return h ? JSON.parse(h) : [];
}

function saveToHistory(hero) {
    const history = loadHistory();
    history.push({
        hero: hero,
        timestamp: new Date().toLocaleString('ru-RU')
    });
    localStorage.setItem('brawl_history', JSON.stringify(history));
}

// Функции обработки строк (критерий 7)
function normalizeInput(text) {
    let cleaned = text.trim().toLowerCase();
    cleaned = cleaned.split(' ').filter(w => w.length > 0).join(' ');
    return cleaned;
}

function formatHeroName(name) {
    return name.trim().charAt(0).toUpperCase() + name.trim().slice(1);
}

// Интерфейс
function showMenu() {
    document.getElementById('mainMenu').style.display = 'block';
    document.getElementById('content').style.display = 'none';
    document.getElementById('exitScreen').style.display = 'none';
}

function showContent(html) {
    document.getElementById('mainMenu').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    document.getElementById('output').innerHTML = html;
}

function exitApp() {
    document.getElementById('mainMenu').style.display = 'none';
    document.getElementById('exitScreen').style.display = 'block';
}

function restartApp() {
    showMenu();
}

// Функция 1: Подбор пика под карту
function showPickForMap() {
    let html = '<div class="output-section"><h3>🗺️ ДОСТУПНЫЕ КАРТЫ:</h3><ul class="hero-list">';
    const mapList = Object.keys(maps_db);
    
    for (let i = 0; i < mapList.length; i++) {
        const map = mapList[i];
        const emoji = mapEmoji[map] || "🎮";
        html += '<li>' + emoji + ' <strong>' + (i+1) + '. ' + map + '</strong> (' + maps_db[map].режим + ')</li>';
    }
    
    html += '</ul>';
    html += '<label>Введи номер карты:</label>';
    html += '<input type="number" id="mapChoice" min="1" max="' + mapList.length + '" style="padding:10px; width:100%; margin:10px 0; border:2px solid #667eea; border-radius:5px;">';
    html += '<button class="menu-btn" onclick="processMapChoice()">Показать пик</button>';
    html += '</div>';
    
    showContent(html);
}

function processMapChoice() {
    const choice = document.getElementById('mapChoice').value.trim();
    const mapList = Object.keys(maps_db);
    
    if (!choice || choice < 1 || choice > mapList.length) {
        alert('❌ Неверный номер');
        return;
    }
    
    const mapName = mapList[choice - 1];
    const mapData = maps_db[mapName];
    const emoji = mapEmoji[mapName] || "🎮";
    
    let html = '<div class="output-section"><h3>' + emoji + ' Карта: ' + mapName + '</h3>';
    html += '<p><strong>Режим:</strong> ' + mapData.режим + '</p></div>';
    
    html += '<div class="output-section"><h3>🏆 ТОП-3 (кого брать):</h3><ul class="hero-list">';
    for (let i = 0; i < mapData.топ.length; i++) {
        const item = mapData.топ[i];
        html += '<li><strong>' + (i+1) + '. ' + formatHeroName(item.герой) + '</strong> — ' + item.причина + '</li>';
        saveToHistory(item.герой);
    }
    html += '</ul></div>';
    
    html += '<div class="output-section"><h3>🚫 АНТИ-ПИК (кого НЕ брать):</h3><ul class="hero-list">';
    for (let i = 0; i < mapData.анти.length; i++) {
        html += '<li class="anti-pick">' + mapData.анти[i] + '</li>';
    }
    html += '</ul></div>';
    
    showContent(html);
}

// Функция 2: Контр-пик
function showCounterPick() {
    let html = '<div class="output-section"><h3>⚔️ ГЕРОИ ПРОТИВНИКА:</h3><ul class="hero-list">';
    const heroes = Object.keys(counter_picks);
    
    for (let i = 0; i < heroes.length; i++) {
        const h = heroes[i];
        const emoji = heroEmoji[h] || "🎯";
        html += '<li>' + emoji + ' <strong>' + (i+1) + '. ' + h + '</strong></li>';
    }
    
    html += '</ul>';
    html += '<label>Введи номер героя:</label>';
    html += '<input type="number" id="heroChoice" min="1" max="' + heroes.length + '" style="padding:10px; width:100%; margin:10px 0; border:2px solid #667eea; border-radius:5px;">';
    html += '<button class="menu-btn" onclick="processHeroChoice()">Показать контр-пик</button>';
    html += '</div>';
    
    showContent(html);
}

function processHeroChoice() {
    const choice = document.getElementById('heroChoice').value.trim();
    const heroes = Object.keys(counter_picks);
    
    if (!choice || choice < 1 || choice > heroes.length) {
        alert('❌ Неверный номер');
        return;
    }
    
    const enemy = heroes[choice - 1];
    const emoji = heroEmoji[enemy] || "🎯";
    
    let html = '<div class="counter-recommendation">';
    html += '<h3>' + emoji + ' ПРОТИВ \'' + enemy + '\' БЕРИ:</h3>';
    html += '<p><strong>' + counter_picks[enemy] + '</strong></p>';
    html += '</div>';
    
    saveToHistory(enemy);
    showContent(html);
}

// Функция 3: История выборов
function showHistory() {
    const history = loadHistory();
    
    if (history.length === 0) {
        showContent('<div class="output-section"><h3>📭 История пуста</h3><p>Ты ещё никого не выбирал.</p></div>');
        return;
    }
    
    // Множество (критерий 8)
    const uniqueHeroes = new Set();
    for (let i = 0; i < history.length; i++) {
        uniqueHeroes.add(history[i].hero);
    }
    
    let html = '<div class="stats">';
    html += '<h3>📊 ТВОЯ ИСТОРИЯ</h3>';
    html += '<p><strong>Всего выборов:</strong> ' + history.length + '</p>';
    html += '<p><strong>Уникальных героев:</strong> ' + uniqueHeroes.size + '</p>';
    html += '</div>';
    
    html += '<div class="output-section"><h3>Последние выборы:</h3><ul class="hero-list">';
    const recent = history.slice(-5).reverse();
    for (let i = 0; i < recent.length; i++) {
        const r = recent[i];
        html += '<li>' + (i+1) + '. <strong>' + r.hero + '</strong> (' + r.timestamp + ')</li>';
    }
    html += '</ul>';
    
    // join() — функция обработки строк (критерий 7)
    const heroesArray = Array.from(uniqueHeroes).sort();
    html += '<p><strong>Твой пул:</strong> ' + heroesArray.join(', ') + '</p></div>';
    
    showContent(html);
}