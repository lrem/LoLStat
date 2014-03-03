CREATE TABLE summoner (
    id INTEGER PRIMARY KEY,
    observed INTEGER NOT NULL DEFAULT 0,
    name STRING
);

CREATE TABLE rank (
    playerOrTeamId INTEGER NOT NULL,
    time INTEGER NOT NULL,
    tier INTEGER NOT NULL, -- This has to be converted from/to text
    division INTEGER NOT NULL, -- Convert from roman numeral 'rank'
    leaguePoints INTEGER NOT NULL
);

CREATE TABLE game (
    gameId INTEGER PRIMARY KEY,
    mapId INTEGER,
    gameMode STRING,
    gameType STRING,
    subType STRING,
    invalid INTEGER,
    createDate INTEGER
);

CREATE TABLE pick (
    gameId INTEGER REFERENCES game,
    championId INTEGER,
    summonerId INTEGER REFERENCES summoner,
    teamId INTEGER,
    PRIMARY KEY (gameId, summonerId)
);

CREATE TABLE stats (
    -- Starting with the key
    summonerId INTEGER REFERENCES summoner,
    gameId INTEGER REFERENCES game,
    -- The first two actually come from the parent object
    spell1 INTEGER,
    spell2 INTEGER,
    -- The rest is a straight dump of the stats object
    assists	INTEGER NOT NULL DEFAULT 0,	
    barracksKilled INTEGER NOT NULL DEFAULT 0,
    championsKilled INTEGER NOT NULL DEFAULT 0,
    combatPlayerScore INTEGER NOT NULL DEFAULT 0,
    consumablesPurchased INTEGER NOT NULL DEFAULT 0,
    damageDealtPlayer INTEGER NOT NULL DEFAULT 0,
    doubleKills INTEGER NOT NULL DEFAULT 0,
    firstBlood INTEGER NOT NULL DEFAULT 0,
    gold INTEGER NOT NULL DEFAULT 0,
    goldEarned INTEGER NOT NULL DEFAULT 0,
    goldSpent INTEGER NOT NULL DEFAULT 0,
    item0 INTEGER NOT NULL DEFAULT 0,
    item1 INTEGER NOT NULL DEFAULT 0,
    item2 INTEGER NOT NULL DEFAULT 0,
    item3 INTEGER NOT NULL DEFAULT 0,
    item4 INTEGER NOT NULL DEFAULT 0,
    item5 INTEGER NOT NULL DEFAULT 0,
    item6 INTEGER NOT NULL DEFAULT 0,
    itemsPurchased INTEGER NOT NULL DEFAULT 0,
    killingSprees INTEGER NOT NULL DEFAULT 0,
    largestCriticalStrike INTEGER NOT NULL DEFAULT 0,
    largestKillingSpree INTEGER NOT NULL DEFAULT 0,
    largestMultiKill INTEGER NOT NULL DEFAULT 0,
    legendaryItemsCreated INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 0,
    magicDamageDealtPlayer INTEGER NOT NULL DEFAULT 0,
    magicDamageDealtToChampions INTEGER NOT NULL DEFAULT 0,
    magicDamageTaken INTEGER NOT NULL DEFAULT 0,
    minionsDenied INTEGER NOT NULL DEFAULT 0,
    minionsKilled INTEGER NOT NULL DEFAULT 0,
    neutralMinionsKilled INTEGER NOT NULL DEFAULT 0,
    neutralMinionsKilledEnemyJungle INTEGER NOT NULL DEFAULT 0,
    neutralMinionsKilledYourJungle INTEGER NOT NULL DEFAULT 0,
    nexusKilled INTEGER NOT NULL DEFAULT 0,
    nodeCapture INTEGER NOT NULL DEFAULT 0,
    nodeCaptureAssist INTEGER NOT NULL DEFAULT 0,
    nodeNeutralize INTEGER NOT NULL DEFAULT 0,
    nodeNeutralizeAssist INTEGER NOT NULL DEFAULT 0,
    numDeaths INTEGER NOT NULL DEFAULT 0,
    numItemsBought INTEGER NOT NULL DEFAULT 0,
    objectivePlayerScore INTEGER NOT NULL DEFAULT 0,
    pentaKills INTEGER NOT NULL DEFAULT 0,
    physicalDamageDealtPlayer INTEGER NOT NULL DEFAULT 0,
    physicalDamageDealtToChampions INTEGER NOT NULL DEFAULT 0,
    physicalDamageTaken INTEGER NOT NULL DEFAULT 0,
    quadraKills INTEGER NOT NULL DEFAULT 0,
    sightWardsBought INTEGER NOT NULL DEFAULT 0,
    spell1Cast INTEGER NOT NULL DEFAULT 0,
    spell2Cast INTEGER NOT NULL DEFAULT 0,
    spell3Cast INTEGER NOT NULL DEFAULT 0,
    spell4Cast INTEGER NOT NULL DEFAULT 0,
    summonSpell1Cast INTEGER NOT NULL DEFAULT 0,
    summonSpell2Cast INTEGER NOT NULL DEFAULT 0,
    superMonsterKilled INTEGER NOT NULL DEFAULT 0,
    team INTEGER NOT NULL DEFAULT 0,
    teamObjective INTEGER NOT NULL DEFAULT 0,
    timePlayed INTEGER NOT NULL DEFAULT 0,
    totalDamageDealt INTEGER NOT NULL DEFAULT 0,
    totalDamageDealtToChampions INTEGER NOT NULL DEFAULT 0,
    totalDamageTaken INTEGER NOT NULL DEFAULT 0,
    totalHeal INTEGER NOT NULL DEFAULT 0,
    totalPlayerScore INTEGER NOT NULL DEFAULT 0,
    totalScoreRank INTEGER NOT NULL DEFAULT 0,
    totalTimeCrowdControlDealt INTEGER NOT NULL DEFAULT 0,
    totalUnitsHealed INTEGER NOT NULL DEFAULT 0,
    tripleKills INTEGER NOT NULL DEFAULT 0,
    trueDamageDealtPlayer INTEGER NOT NULL DEFAULT 0,
    trueDamageDealtToChampions INTEGER NOT NULL DEFAULT 0,
    trueDamageTaken INTEGER NOT NULL DEFAULT 0,
    turretsKilled INTEGER NOT NULL DEFAULT 0,
    unrealKills INTEGER NOT NULL DEFAULT 0,
    victoryPointTotal INTEGER NOT NULL DEFAULT 0,
    visionWardsBought INTEGER NOT NULL DEFAULT 0,
    wardKilled INTEGER NOT NULL DEFAULT 0,
    wardPlaced INTEGER NOT NULL DEFAULT 0,
    win INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (gameId, summonerId)
);
