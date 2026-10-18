from datetime import date
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).parent
app = FastAPI(title='Cosmic Birthday API', version='1.0.0')
app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')

SIGNS = [
 ('Capricorn','♑','Earth','Saturn','Ambitious, disciplined, dependable','Brown','4, 8, 13','Taurus, Virgo','The sea-goat combines a goat and fish in one mythical symbol.'),
 ('Aquarius','♒','Air','Uranus','Inventive, independent, curious','Electric blue','4, 7, 11','Gemini, Libra','Aquarius is an air sign despite its Water Bearer symbol.'),
 ('Pisces','♓','Water','Neptune','Empathetic, imaginative, gentle','Sea green','3, 7, 12','Cancer, Scorpio','Two fish symbolize Pisces, often swimming in opposite directions.'),
 ('Aries','♈','Fire','Mars','Brave, ambitious, energetic','Red','1, 9, 17','Leo, Sagittarius','Aries marks the beginning of the traditional Western zodiac.'),
 ('Taurus','♉','Earth','Venus','Loyal, patient, determined','Emerald green','2, 6, 15, 24','Virgo, Capricorn','Taurus is ruled by Venus, traditionally linked with beauty.'),
 ('Gemini','♊','Air','Mercury','Witty, adaptable, social','Yellow','3, 5, 14','Libra, Aquarius','Gemini is associated with the twins Castor and Pollux.'),
 ('Cancer','♋','Water','Moon','Protective, caring, intuitive','Silver','2, 7, 11','Scorpio, Pisces','Cancer is the only sign traditionally ruled by the Moon.'),
 ('Leo','♌','Fire','Sun','Warm, expressive, confident','Gold','1, 5, 19','Aries, Sagittarius','The lion represents Leo, traditionally linked to the Nemean lion.'),
 ('Virgo','♍','Earth','Mercury','Thoughtful, analytical, practical','Olive green','3, 5, 14','Taurus, Capricorn','Virgo is traditionally shown as a maiden holding wheat.'),
 ('Libra','♎','Air','Venus','Fair, artistic, diplomatic','Pink','6, 9, 15','Gemini, Aquarius','Libra is the only zodiac represented by an inanimate object.'),
 ('Scorpio','♏','Water','Pluto','Focused, passionate, resourceful','Burgundy','8, 9, 18','Cancer, Pisces','Scorpio is also linked to the eagle and phoenix in some traditions.'),
 ('Sagittarius','♐','Fire','Jupiter','Optimistic, adventurous, candid','Purple','3, 7, 21','Aries, Leo','Sagittarius is depicted as an archer, often a centaur.'),
]
GEMS = [
 ('Garnet','Protection and friendship','Garnet gets its name from a word associated with pomegranate seeds.'),
 ('Amethyst','Calm and clarity','Amethyst was historically associated with clear thinking.'),
 ('Aquamarine','Serenity and courage','Aquamarine means sea water.'),
 ('Diamond','Strength and enduring love','Diamonds are the hardest natural mineral on the Mohs scale.'),
 ('Emerald','Growth and renewal','Cleopatra was famously fond of emeralds.'),
 ('Pearl','Wisdom and harmony','Natural pearls grow inside certain mollusks.'),
 ('Ruby','Passion and vitality','Ruby and sapphire belong to the corundum mineral family.'),
 ('Peridot','Joy and positivity','Some peridot crystals come from meteorites.'),
 ('Sapphire','Truth and loyalty','Sapphires naturally occur in multiple colors.'),
 ('Opal','Creativity and wonder','Precious opal can show many rainbow colors.'),
 ('Topaz','Friendship and warmth','Topaz occurs in several different colors.'),
 ('Turquoise','Good fortune and protection','Turquoise has been treasured for millennia.'),
]
FLOWERS = ['Carnation and snowdrop','Violet and primrose','Daffodil','Daisy and sweet pea','Lily of the valley','Rose and honeysuckle','Larkspur and water lily','Gladiolus and poppy','Aster and morning glory','Marigold and cosmos','Chrysanthemum','Narcissus and holly']
ANIME = {
 'Naruto': [('Naruto Uzumaki','bold','A never-give-up fighter who puts friends first.'),('Shikamaru Nara','strategic','A thoughtful strategist who values calm planning.'),('Hinata Hyuga','caring','A quietly brave and loyal friend.'),('Kakashi Hatake','curious','An observant mentor with a playful side.')],
 'One Piece': [('Monkey D. Luffy','bold','A freedom-loving adventurer loyal to his crew.'),('Nico Robin','strategic','A calm intellectual who solves mysteries.'),('Tony Tony Chopper','caring','An empathetic friend who wants to help others.'),('Usopp','curious','A creative storyteller with surprising courage.')],
 'Spy x Family': [('Anya Forger','curious','An imaginative, playful character with endless curiosity.'),('Loid Forger','strategic','A calm planner who protects the people around him.'),('Yor Forger','caring','A gentle but fiercely protective and devoted person.'),('Yuri Briar','bold','An intense and determined character who acts on conviction.')],
 'Demon Slayer': [('Inosuke Hashibira','bold','A bold, competitive spirit who charges into challenges.'),('Shinobu Kocho','strategic','A clever tactician with keen observation.'),('Tanjiro Kamado','caring','A compassionate protector who never abandons loved ones.'),('Zenitsu Agatsuma','curious','An emotional and surprisingly resourceful friend.')],
 'Jujutsu Kaisen': [('Yuji Itadori','caring','An empathetic hero who helps others.'),('Megumi Fushiguro','strategic','Reserved, principled and calculated.'),('Nobara Kugisaki','bold','Confident, fearless and independent.'),('Satoru Gojo','curious','Playful, inventive and unconventional.')],
 'Attack on Titan': [('Eren Yeager','bold','Fiercely driven and unwilling to give up.'),('Armin Arlert','strategic','A perceptive thinker who looks for possibilities.'),('Mikasa Ackerman','caring','Exceptionally loyal and protective.'),('Hange Zoë','curious','Passionately curious about the unknown.')],
 'Death Note': [('Mello','bold','An ambitious risk-taker.'),('L','strategic','A brilliant observer who follows evidence.'),('Soichiro Yagami','caring','A devoted protector with a strong sense of duty.'),('Near','curious','An analytical problem-solver fascinated by puzzles.')],
 'Dragon Ball': [('Son Goku','bold','An enthusiastic adventurer who loves a challenge.'),('Piccolo','strategic','A patient mentor who plans carefully.'),('Gohan','caring','A gentle scholar and protective fighter.'),('Bulma','curious','An inventive explorer and problem solver.')],
 'Bleach': [('Ichigo Kurosaki','bold','A determined fighter who protects friends.'),('Uryū Ishida','strategic','A meticulous and principled tactician.'),('Orihime Inoue','caring','Kind, compassionate and supportive.'),('Kisuke Urahara','curious','Inventive and interested in puzzles.')],
 'My Hero Academia': [('Katsuki Bakugo','bold','Competitive and fiercely driven.'),('Momo Yaoyorozu','strategic','An intelligent and prepared leader.'),('Izuku Midoriya','caring','A thoughtful hero who wants to save people.'),('Mei Hatsume','curious','An inventive and energetic creator.')],
 'Hunter x Hunter': [('Gon Freecss','bold','Adventurous and fearless.'),('Kurapika','strategic','A disciplined and insightful planner.'),('Leorio Paradinight','caring','A loyal friend who wants to help others.'),('Killua Zoldyck','curious','Quick-thinking and adaptable.')],
 'Haikyuu!!': [('Shoyo Hinata','bold','Enthusiastic and driven to improve.'),('Kenma Kozume','strategic','Observant, cerebral and calm.'),('Daichi Sawamura','caring','A reliable and protective teammate.'),('Toru Oikawa','curious','Social, perceptive and always learning.')],
 'Blue Lock': [('Meguru Bachira','curious','Creative, unpredictable and playful.'),('Yoichi Isagi','strategic','An analytical player who adapts quickly.'),('Rensuke Kunigami','caring','Principled and dependable.'),('Shoei Baro','bold','Determined and exceptionally competitive.')],
 'Chainsaw Man': [('Power','bold','Loud, fearless and impulsive.'),('Aki Hayakawa','strategic','Serious, practical and highly disciplined.'),('Denji','curious','Spontaneous and eager to discover life.'),('Kobeni Higashiyama','caring','Sensitive and deeply concerned for others.')],
 'Solo Leveling': [('Sung Jinwoo','strategic','Patient, adaptable and consistently improving.'),('Cha Hae-in','caring','Loyal, brave and principled.'),('Yoo Jinho','curious','Optimistic and eager to learn.'),('Baek Yoonho','bold','Powerful, decisive and protective.')],
 'Black Clover': [('Asta','bold','Tenacious and determined.'),('Yuno','strategic','Calm, focused and disciplined.'),('Mimosa Vermillion','caring','Supportive and gentle.'),('Julius Novachrono','curious','Fascinated by discovering new powers.')],
 'One Punch Man': [('Saitama','bold','Unfazed by daunting challenges.'),('Genos','strategic','Focused on improvement and careful analysis.'),('Mumen Rider','caring','Selfless and dependable.'),('Child Emperor','curious','An inventive young genius.')],
 'Vinland Saga': [('Thorfinn','bold','Determined and resilient.'),('Askeladd','strategic','A brilliant and complex tactician.'),('Einar','caring','Kind and grounded in friendship.'),('Leif Erikson','curious','An explorer who loves stories and discovery.')],
 'Pokémon': [('Ash Ketchum','bold','Energetic and always ready for adventure.'),('Cynthia','strategic','Calm and deeply knowledgeable.'),('Brock','caring','A dependable and thoughtful friend.'),('Professor Oak','curious','A researcher who loves learning about Pokémon.')],
}
TRAITS = ['bold','strategic','caring','curious']

class ProfileRequest(BaseModel):
    birthday: date
    anime: str
    compare_sign: str = 'Virgo'

def zodiac_index(m,d):
    boundaries = [19,18,20,19,20,20,22,22,22,22,21,21]
    before = [0,1,2,3,4,5,6,7,8,9,10,11]
    return before[m-1] if d <= boundaries[m-1] else (before[m-1]+1)%12

def chinese_year(bday):
    # Chinese New Year dates for supported recent years; fallback year is not presumed exact.
    new_years = {2000:(2,5),2001:(1,24),2002:(2,12),2003:(2,1),2004:(1,22),2005:(2,9),2006:(1,29),2007:(2,18),2008:(2,7),2009:(1,26),2010:(2,14),2011:(2,3),2012:(1,23),2013:(2,10),2014:(1,31),2015:(2,19),2016:(2,8),2017:(1,28),2018:(2,16),2019:(2,5),2020:(1,25),2021:(2,12),2022:(2,1),2023:(1,22),2024:(2,10),2025:(1,29),2026:(2,17)}
    if bday.year not in new_years: return 'Chinese zodiac not available for this birth year in the offline data set'
    year = bday.year
    if (bday.month,bday.day)<new_years[year]: year -= 1
    animals=['Rat','Ox','Tiger','Rabbit','Dragon','Snake','Horse','Goat','Monkey','Rooster','Dog','Pig']
    elements=['Wood','Fire','Earth','Metal','Water']
    return f'{elements[((year-4)%10)//2]} {animals[(year-4)%12]}'

@app.get('/')
def index(): return FileResponse(ROOT/'static'/'index.html')

@app.get('/api/options')
def options(): return {'anime': sorted(ANIME),'signs':[s[0] for s in SIGNS]}

@app.post('/api/profile')
def profile(req: ProfileRequest):
    if req.birthday < date(1900,1,1) or req.birthday > date.today():
        raise HTTPException(400,'Enter a valid birth date between 1900 and today.')
    if req.anime not in ANIME:
        raise HTTPException(400,'Choose a valid anime.')
    if req.compare_sign not in [s[0] for s in SIGNS]:
        raise HTTPException(400,'Choose a valid comparison sign.')
    idx=zodiac_index(req.birthday.month,req.birthday.day)
    s=SIGNS[idx]
    other=SIGNS[[i for i,x in enumerate(SIGNS) if x[0]==req.compare_sign][0]]
    gem=GEMS[req.birthday.month-1]
    candidates=ANIME[req.anime]
    # Deterministic, entertainment-only match derived from birthday and sign; no self-rating questionnaire.
    archetypes = {'Earth':['caring','strategic','curious','bold'],'Water':['caring','curious','strategic','bold'],'Fire':['bold','curious','caring','strategic'],'Air':['curious','strategic','bold','caring']}
    trait = archetypes[s[2]][(req.birthday.day + req.birthday.month) % 4]
    match = next(c for c in candidates if c[1] == trait)
    digits=sum(int(c) for c in req.birthday.isoformat() if c.isdigit())
    life=digits
    while life>9 and life not in (11,22,33): life=sum(map(int,str(life)))
    next_bday_year=date.today().year
    try: upcoming=date(next_bday_year,req.birthday.month,req.birthday.day)
    except ValueError: upcoming=date(next_bday_year,3,1)
    if upcoming<date.today():
        try: upcoming=date(next_bday_year+1,req.birthday.month,req.birthday.day)
        except ValueError: upcoming=date(next_bday_year+1,3,1)
    return {
      'birthday':req.birthday.isoformat(),'weekday':req.birthday.strftime('%A'),
      'age':date.today().year-req.birthday.year-((date.today().month,date.today().day)<(req.birthday.month,req.birthday.day)),
      'next_birthday':upcoming.isoformat(),'days_until_birthday':(upcoming-date.today()).days,
      'zodiac':{'name':s[0],'symbol':s[1],'element':s[2],'ruler':s[3],'traits':s[4],'color':s[5],'numbers':s[6],'matches':s[7],'fact':s[8]},
      'birthstone':{'name':gem[0],'meaning':gem[1],'fact':gem[2]},
      'birth_flower':FLOWERS[req.birthday.month-1], 'life_path':str(life),
      'chinese_zodiac':chinese_year(req.birthday),
      'compatibility':{'sign':other[0],'symbol':other[1], 'score': 91 if s[2]==other[2] else 82 if {s[2],other[2]} in ({'Water','Earth'},{'Fire','Air'}) else 69, 'description': 'A playful match based on traditional element pairings, not a scientific compatibility score.'},
      'character':{'name':match[0],'description':match[2], 'score': 85+((req.birthday.day+idx)%12), 'anime':req.anime},
      'note':'Astrology, lucky numbers, numerology and anime matches are for entertainment.'
    }
