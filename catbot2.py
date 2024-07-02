import discord
import requests
from discord.ext import commands
from discord import app_commands
import asyncio

# GitHub dosya URL'si

BAD_WORDS = [
    "abaza", "abazan", "ag", "ağzına sıçayım", "ahmak", "allah", "allahsız", "am", "sg", "amarım",
    "ambiti", "am biti", "amcığı", "amcığın", "amcığını", "amcığınızı", "amcık", "amcık hoşafı",
    "amcıklama", "amcıklandı", "amcik", "amck", "amckl", "amcklama", "amcklaryla", "amckta",
    "amcktan", "amcuk", "amık", "amına", "amınako", "amına koy", "amına koyarım", "amına koyayım",
    "amınakoyim", "amına koyyim", "amına s", "amına sikem", "amına sokam", "amın feryadı", "amını",
    "amını s", "amın oglu", "amınoğlu", "amın oğlu", "amısına", "amısını", "amina", "amina g",
    "amina k", "aminako", "aminakoyarim", "amina koyarim", "amina koyayım", "amina koyayim",
    "aminakoyim", "aminda", "amindan", "amindayken", "amini", "aminiyarraaniskiim", "aminoglu",
    "amin oglu", "amiyum", "amk", "amkafa", "amk çocuğu", "amlarnzn", "amlı", "amm", "ammak",
    "ammna", "amn", "amna", "amnda", "amndaki", "amngtn", "amnn", "amona", "amq", "amsız", "amsiz",
    "amsz", "amteri", "amugaa", "amuğa", "amuna", "ana", "anaaann", "anal", "analarn", "anam",
    "anamla", "anan", "anana", "anandan", "ananı", "ananı ", "ananın", "ananın am", "ananın amı",
    "ananın dölü", "ananınki", "ananısikerim", "ananı sikerim", "ananısikeyim", "ananı sikeyim",
    "ananızın", "ananızın am", "anani", "ananin", "ananisikerim", "anani sikerim", "ananisikeyim",
    "anani sikeyim", "anann", "ananz", "anas", "anasını", "anasının am", "anası orospu", "anasi",
    "anasinin", "anay", "anayin", "angut", "anneni", "annenin", "annesiz", "anuna", "aptal", "aq",
    "a.q", "a.q.", "aq.", "ass", "atkafası", "atmık", "attırdığım", "attrrm", "auzlu", "avrat",
    "ayklarmalrmsikerim", "azdım", "azdır", "azdırıcı", "babaannesi kaşar", "babanı", "babanın",
    "babani", "babası pezevenk", "bacağına sıçayım", "bacına", "bacını", "bacının", "bacini",
    "bacn", "bacndan", "bacy", "bastard", "basur", "beyinsiz", "bızır", "bitch", "biting", "bok",
    "boka", "bokbok", "bokça", "bokhu", "bokkkumu", "boklar", "boktan", "boku", "bokubokuna", "bokum",
    "bombok", "boner", "bosalmak", "boşalmak", "cenabet", "cibiliyetsiz", "cibilliyetini",
    "cibilliyetsiz", "cif", "cikar", "cim", "çük", "dalaksız", "dallama", "daltassak", "dalyarak",
    "dalyarrak", "dangalak", "dassagi", "diktim", "dildo", "dingil", "dingilini", "dinsiz", "dkerim",
    "domal", "domalan", "domaldı", "domaldın", "domalık", "domalıyor", "domalmak", "domalmış",
    "domalsın", "domalt", "domaltarak", "domaltıp", "domaltır", "domaltırım", "domaltip", "domaltmak",
    "dölü", "dönek", "düdük", "eben", "ebeni", "ebenin", "ebeninki", "ebleh", "ecdadını", "ecdadini",
    "embesil", "emi", "fahise", "fahişe", "feriştah", "ferre", "fuck", "fucker", "fuckin", "fucking",
    "gavad", "gavat", "geber", "geberik", "gebermek", "gebermiş", "gebertir", "gerızekalı",
    "gerizekalı", "gerizekali", "gerzek", "giberim", "giberler", "gibis", "gibiş", "gibmek", "gibtiler",
    "goddamn", "godoş", "godumun", "gotelek", "gotlalesi", "gotlu", "gotten", "gotundeki", "gotunden",
    "gotune", "gotunu", "gotveren", "goyiim", "goyum", "goyuyim", "goyyim", "göt", "göt deliği",
    "götelek", "göt herif", "götlalesi", "götlek", "götoğlanı", "göt oğlanı", "götoş", "götten",
    "götü", "götün", "götüne", "götünekoyim", "götüne koyim", "götünü", "götveren", "göt veren",
    "göt verir", "gtelek", "gtn", "gtnde", "gtnden", "gtne", "gtten", "gtveren", "hasiktir",
    "hassikome", "hassiktir", "has siktir", "hassittir", "haysiyetsiz", "hayvan herif", "hoşafı",
    "hödük", "hsktr", "huur", "ıbnelık", "ibina", "ibine", "ibinenin", "ibne", "ibnedir", "ibneleri",
    "ibnelik", "ibnelri", "ibneni", "ibnenin", "ibnerator", "ibnesi", "idiot", "idiyot", "imansz",
    "ipne", "iserim", "işerim", "itoğlu it", "kafam girsin", "kafasız", "kafasiz", "kahpe", "kahpenin",
    "kahpenin feryadı", "kaka", "kaltak", "kancık", "kancik", "kappe", "karhane", "kaşar", "kavat",
    "kavatn", "kaypak", "kayyum", "kerane", "kerhane", "kerhanelerde", "kevase", "kevaşe", "kevvase",
    "koca göt", "koduğmun", "koduğmunun", "kodumun", "kodumunun", "koduumun", "koyarm", "koyayım",
    "koyiim", "koyiiym", "koyim", "koyum", "koyyim", "krar", "kukudaym", "laciye boyadım", "lavuk",
    "liboş", "madafaka", "mal", "malafat", "malak", "manyak", "mcik", "meme", "memelerini",
    "mezveleli", "minaamcık", "mincikliyim", "mna", "monakkoluyum", "motherfucker", "mudik", "oc",
    "ocuu", "ocuun", "OÇ", "oç", "o. çocuğu", "oğlan", "oğlancı", "oğlu it", "orosbucocuu", "orospu",
    "orospucocugu", "orospu cocugu", "orospu çoc", "orospuçocuğu", "orospu çocuğu", "orospu çocuğudur",
    "orospu çocukları", "orospudur", "orospular", "ospunun", "orospunun evladı", "orospuydu", "orospuyuz", "orostoban", "orostopol", "orrospu",
    "oruspu", "oruspuçocuğu", "oruspu çocuğu", "osbir", "ossurduum", "ossurmak", "ossuruk", "osur",
    "osurduu", "osuruk", "osururum", "otuzbir", "öküz", "öşex", "patlak zar", "penis", "pezevek",
    "pezeven", "pezeveng", "pezevengi", "pezevengin evladı", "pezevenk", "pezo", "pic", "pici",
    "picler", "piç", "piçin oğlu", "piç kurusu", "piçler", "pipi", "pipiş", "pisliktir", "porno",
    "pussy", "puşt", "puşttur", "rahminde", "revizyonist", "s1kerim", "s1kerm", "s1krm", "sakso",
    "saksofon", "salaak", "salak", "saxo", "sekis", "serefsiz", "sevgi koyarım", "sevişelim", "sexs",
    "sıçarım", "sıçtığım", "sıecem", "sicarsin", "sie", "sik", "sikdi", "sikdiğim", "sike", "sikecem",
    "sikem", "siken", "sikenin", "siker", "sikerim", "sikerler", "sikersin", "sikertir", "sikertmek",
    "sikesen", "sikesicenin", "sikey", "sikeydim", "sikeyim", "sikeym", "siki", "sikicem", "sikici",
    "sikien", "sikienler", "sikiiim", "sikiiimmm", "sikiim", "sikiir", "sikiirken", "sikik", "sikil",
    "sikildiini", "sikilesice", "sikilmi", "sikilmie", "sikilmis", "sikilmiş", "sikilsin", "sikim",
    "sikimde", "sikimden", "sikime", "sikimi", "sikimiin", "sikimin", "sikimle", "sikimsonik",
    "sikimtrak", "sikin", "sikinde", "sikinden", "sikine", "sikini", "sikip", "sikis", "sikisek",
    "sikisen", "sikish", "sikismis", "sikiş", "sikişen", "sikişme", "sikitiin", "sikiyim", "sikiym",
    "sikiyorum", "sikkim", "sikko", "sikleri", "sikleriii", "sikli", "sikm", "sikmek", "sikmem",
    "sikmiler", "sikmisligim", "siksem", "sikseydin", "sikseyidin", "siksin", "siksinbaya", "siksinler",
    "siksiz", "siksok", "siksz", "sikt", "sikti", "siktigimin", "siktigiminin", "siktiğim",
    "siktiğimin", "siktiğiminin", "siktii", "siktiim", "siktiimin", "siktiiminin", "siktiler",
    "siktim", "siktim", "siktimin", "siktiminin", "siktir", "siktir et", "siktirgit", "siktir git",
    "siktirir", "siktiririm", "siktiriyor", "siktir lan", "siktirolgit", "siktir ol git", "sittimin",
    "sittir", "skcem", "skecem", "skem", "sker", "skerim", "skerm", "skeyim", "skiim", "skik", "skim",
    "skime", "skmek", "sksin", "sksn", "sksz", "sktiimin", "sktrr", "skyim", "slaleni", "sokam",
    "sokarım", "sokarim", "sokarm", "sokarmkoduumun", "sokayım", "sokaym", "sokiim", "soktuğumunun",
    "sokuk", "sokum", "sokuş", "sokuyum", "soxum", "sulaleni", "sülaleni", "sülalenizi", "sürtük",
    "şerefsiz", "şıllık", "taaklarn", "taaklarna", "tarrakimin", "tasak", "tassak", "taşak", "taşşak",
    "tipini s.k", "tipinizi s.keyim", "tiyniyat", "toplarm", "topsun", "totoş", "vajina", "vajinanı",
    "veled", "veledizina", "veled i zina", "verdiimin", "weled", "weledizina", "whore", "xikeyim",
    "yaaraaa", "yalama", "yalarım", "yalarun", "yaraaam", "yarak", "yaraksız", "yaraktr", "yaram",
    "yaraminbasi", "yaramn", "yararmorospunun", "yarra", "yarraaaa", "yarraak", "yarraam", "yarraamı",
    "yarragi", "yarragimi", "yarragina", "yarragindan", "yarragm", "yarrağ", "yarrağım", "yarrağımı",
    "yarraimin", "yarrak", "yarram", "yarramin", "yarraminbaşı", "yarramn", "yarran", "yarrana",
    "yarrrak", "yavak", "yavş", "yavşak", "yavşaktır", "yavuşak", "yılışık", "yilisik", "yogurtlayam",
    "yoğurtlayam", "yrrak", "zıkkımım", "zibidi", "zigsin", "zikeyim", "zikiiim", "zikiim", "zikik",
    "zikim", "ziksiiin", "ziksiin", "zulliyetini", "zviyetini", "2g1c", "2 girls 1 cup", "acrotomophilia", "alabama hot pocket", "alaskan pipeline", "anal",
    "anilingus", "anus", "apeshit", "arsehole", "ass", "asshole", "assmunch", "auto erotic",
    "autoerotic", "babeland", "baby batter", "baby juice", "ball gag", "ball gravy", "ball kicking",
    "ball licking", "ball sack", "ball sucking", "bangbros", "bangbus", "bareback", "barely legal",
    "barenaked", "bastard", "bastardo", "bastinado", "bbw", "bdsm", "beaner", "beaners",
    "beaver cleaver", "beaver lips", "beastiality", "bestiality", "big black", "big breasts",
    "big knockers", "big tits", "bimbos", "birdlock", "bitch", "bitches", "black cock", "blonde action",
    "blonde on blonde action", "blowjob", "blow job", "blow your load", "blue waffle", "blumpkin",
    "bollocks", "bondage", "boner", "boob", "boobs", "booty call", "brown showers", "brunette action",
    "bukkake", "bulldyke", "bullet vibe", "bullshit", "bung hole", "bunghole", "busty", "butt",
    "buttcheeks", "butthole", "camel toe", "camgirl", "camslut", "camwhore", "carpet muncher",
    "carpetmuncher", "chocolate rosebuds", "cialis", "circlejerk", "cleveland steamer", "clit",
    "clitoris", "clover clamps", "clusterfuck", "cock", "cocks", "coprolagnia", "coprophilia",
    "cornhole", "coon", "coons", "creampie", "cum", "cumming", "cumshot", "cumshots", "cunnilingus",
    "cunt", "darkie", "date rape", "daterape", "deep throat", "deepthroat", "dendrophilia", "dick",
    "dildo", "dingleberry", "dingleberries", "dirty pillows", "dirty sanchez", "doggie style",
    "doggiestyle", "doggy style", "doggystyle", "dog style", "dolcett", "domination", "dominatrix",
    "dommes", "donkey punch", "double dong", "double penetration", "dp action", "dry hump", "dvda",
    "eat my ass", "ecchi", "ejaculation", "erotic", "erotism", "escort", "eunuch", "fag", "faggot",
    "fecal", "felch", "fellatio", "feltch", "female squirting", "femdom", "figging", "fingerbang",
    "fingering", "fisting", "foot fetish", "footjob", "frotting", "fuck", "fuck buttons", "fuckin",
    "fucking", "fucktards", "fudge packer", "fudgepacker", "futanari", "gangbang", "gang bang",
    "gay sex", "genitals", "giant cock", "girl on", "girl on top", "girls gone wild", "goatcx",
    "goatse", "god damn", "gokkun", "golden shower", "goodpoop", "goo girl", "goregasm", "grope",
    "group sex", "g-spot", "guro", "hand job", "handjob", "hard core", "hardcore", "hentai",
    "homoerotic", "honkey", "hooker", "horny", "hot carl", "hot chick", "how to kill", "how to murder",
    "huge fat", "humping", "incest", "intercourse", "jack off", "jail bait", "jailbait", "jelly donut",
    "jerk off", "jigaboo", "jiggaboo", "jiggerboo", "jizz", "juggs", "kike", "kinbaku", "kinkster",
    "kinky", "knobbing", "leather restraint", "leather straight jacket", "lemon party", "livesex",
    "lolita", "lovemaking", "make me come", "male squirting", "masturbate", "masturbating",
    "masturbation", "menage a trois", "milf", "missionary position", "mong", "motherfucker",
    "mound of venus", "mr hands", "muff diver", "muffdiving", "nambla", "nawashi", "negro", "neonazi",
    "nigga", "nigger", "nig nog", "nimphomania", "nipple", "nipples", "nsfw", "nsfw images", "nude",
    "nudity", "nutten", "nympho", "nymphomania", "octopussy", "omorashi", "one cup two girls",
    "one guy one jar", "orgasm", "orgy", "paedophile", "paki", "panties", "panty", "pedobear",
    "pedophile", "pegging", "penis", "phone sex", "piece of shit", "pikey", "pissing", "piss pig",
    "pisspig", "playboy", "pleasure chest", "pole smoker", "ponyplay", "poof", "poon", "poontang",
    "punany", "poop chute", "poopchute", "porn", "porno", "pornography", "prince albert piercing",
    "pthc", "pubes", "pussy", "queaf", "queef", "quim", "raghead", "raging boner", "rape", "raping",
    "rapist", "rectum", "reverse cowgirl", "rimjob", "rimming", "rosy palm", "rosy palm and her 5 sisters",
    "rusty trombone", "sadism", "santorum", "scat", "schlong", "scissoring", "semen", "sex", "sexcam",
    "sexo", "sexy", "sexual", "sexually", "sexuality", "shaved beaver", "shaved pussy", "shemale",
    "shibari", "shit", "shitblimp", "shitty", "shota", "shrimping", "skeet", "slanteye", "slut", "s&m",
    "smut", "snatch", "snowballing", "sodomize", "sodomy", "spastic", "spic", "splooge", "splooge moose", "spooge", "spread legs", "spunk", "strap on", "strapon", "strappado", "strip club", "style doggy", "suck", "sucks", "suicide girls", "sultry women", "swastika", "swinger", "tainted love", "taste my", "tea bagging", "threesome", "throating", "thumbzilla", "tied up", "tight white", "tit", "tits", "titties", "titty", "tongue in a", "topless", "tosser", "towelhead", "tranny", "tribadism", "tub girl", "tubgirl", "tushy", "twat", "twink", "twinkie", "two girls one cup", "undressing", "upskirt",
    "urethra play", "urophilia", "vagina", "venus mound", "viagra", "vibrator", "violet wand", "vorarephilia", "voyeur", "voyeurweb", "voyuer", "vulva", "wank", "wetback", "wet dream", "white power", "whore", "worldsex", "wrapping men", "wrinkled starfish", "xx", "xxx", "yaoi", "yellow showers", "yiffy", "zoophilia", "سكس", "طيز", "شرج", "لعق", "لحس", "مص", "تمص", "بيضان", "ثدي", "بز", "بزاز", "حلمة", "مفلقسة", "بظر", "كس", "فرج", "شهوة", "شاذ", "مبادل", "عاهرة", "جماع", "قضيب", "زب", "لوطي", "لواط", "سحاق", "سحاقية", "اغتصاب", "خنثي", "احتلام", "نيك", "متناك", "متناكة", "شرموطة", "عرص", "خول", "قحبة", "لبوة", "bordel", "buzna", "čumět", "čurák", "debil", "do piče", "do prdele", "dršťka", "držka", "flundra", "hajzl", "hovno", "chcanky", "chuj", "jebat", "kokot", "kokotina", "koňomrd", "kunda", "kurva", "mamrd", "mrdat", "mrdka", "mrdník", "oslošoust", "piča", "píčus", "píchat", "pizda", "prcat", "prdel", "prdelka", "sračka", "srát", "šoustat", "šulin", "vypíčenec", "zkurvit", "zkurvysyn", "zmrd", "žrát", "anus", "bøsserøv", "cock", "fisse", "fissehår", "fuck", "hestepik", "kussekryller", "lort", "luder", "pik", "pikhår", "pikslugeri", "piksutteri", "pis", "røv", "røvhul", "røvskæg", "røvspræke", "shit",  "analritter", "arsch", "arschficker", "arschlecker", "arschloch", "bimbo", "bratze", "bumsen", "bonze", "dödel", "fick", "ficken", "flittchen", "fotze", "fratze", "hackfresse", "hure", "hurensohn", "ische", "kackbratze", "kacke", "kacken", "kackwurst", "kampflesbe", "kanake", "kimme", "lümmel", "MILF", "möpse", "morgenlatte", "möse", "mufti", "muschi", "nackt", "neger", "nigger", "nippel", "nutte", "onanieren", "orgasmus", "penis", "pimmel", "pimpern", "pinkeln", "pissen", "pisser", "popel", "poppen", "porno", "reudig", "rosette", "schabracke", "schlampe", "scheiße", "scheisser", "schiesser", "schnackeln", "schwanzlutscher", "schwuchtel", "tittchen", "titten", "vögeln", "vollpfosten", "wichse", "wichsen", "wichser",  "Asesinato", "asno", "bastardo", "Bollera", "Cabrón", "Caca", "Chupada", "Chupapollas", "Chupetón", "concha", "Concha de tu madre", "Coño", "Coprofagía", "Culo", "Drogas", "Esperma", "Fiesta de salchichas", "Follador", "Follar", "Gilipichis", "Gilipollas", "Hacer una paja", "Haciendo el amor", "Heroína", "Hija de puta", "Hijaputa", "Hijo de puta", "Hijoputa", "Idiota", "Imbécil", "infierno", "Jilipollas", "Kapullo", "Lameculos", "Maciza", "Macizorra", "maldito", "Mamada", "Marica", "Maricón", "Mariconazo", "martillo", "Mierda", "Nazi", "Orina", "Pedo", "Pendejo", "Pervertido", "Pezón", "Pinche", "Pis", "Prostituta", "Puta", "Racista", "Ramera", "Sádico", "Semen", "Sexo", "Sexo oral", "Soplagaitas", "Soplapollas", "Tetas grandes", "Tía buena", "Travesti", "Trio", "Verga", "vete a la mierda", "Vulva", "آب کیر", "ارگاسم", "برهنه", "پورن", "پورنو", "تجاوز", "تخمی", "جق", "جقی", "جلق", "جنده", "چوچول", "حشر", "حشری", "داف", "دودول", "ساک زدن", "سکس", "سکس کردن", "سکسی", "سوپر", "شق کردن", "شهوت", "شهوتی", "شونبول", "فیلم سوپر", "کس", "کس دادن", "کس کردن", "کسکش", "کوس", "کون", "کون دادن", "کون کردن", "کونکش", "کونی", "کیر", "کیری", "لاپا", "لاپایی", "لاشی", "لخت", "لش", "منی", "هرزه", "alfred nussi", "bylsiä", "haahka", "haista paska", "haista vittu", "hatullinen", "helvetisti", "hevonkuusi", "hevonpaska", "hevonperse", "hevonvittu", "hevonvitunperse", "hitosti", "hitto", "huorata", "hässiä", "juosten kustu", "jutku", "jutsku", "jätkä", "kananpaska", "koiranpaska", "kuin esterin perseestä", "kulli", "kullinluikaus", "kuppainen", "kusaista", "kuseksia", "kusettaa", "kusi", "kusipää", "kusta", "kyrpiintynyt", "kyrpiintyä", "kyrpiä", "kyrpä", "kyrpänaama", "kyrvitys", "lahtari", "lutka", "molo", "molopää", "mulkero", "mulkku", "mulkvisti", "muna", "munapää", "munaton", "mutakuono", "mutiainen", "naida", "nainti", "narttu", "neekeri", "nekru", "nuolla persettä", "nussia", "nussija", "nussinta", "paljaalla", "palli", "pallit", "paneskella", "panettaa", "panna", "pano", "pantava", "paska", "paskainen", "paskamainen", "paskanmarjat", "paskantaa", "paskapuhe", "paskapää", "paskattaa", "paskiainen", "paskoa", "pehko", "pentele", "perkele", "perkeleesti", "persaukinen", "perse", "perseennuolija", "perseet olalla", "persereikä", "perseääliö", "persläpi", "perspano", "persvako", "pilkunnussija", "pillu", "pillut", "pipari", "piru", "pistää", "pyllyvako", "reikä", "reva", "ripsipiirakka", "runkata", "runkkari", "runkkaus", "runkku", "ryssä", "rättipää", "saatanasti", "suklaaosasto", "tavara", "toosa", "tuhkaluukku", "tumputtaa", "turpasauna", "tussu", "tussukka", "tussut", "vakipano", "vetää käteen", "viiksi", "vittu", "vittuilla", "vittuilu", "vittumainen", "vittuuntua", "vittuuntunut", "vitun", "vitusti", "vituttaa", "vitutus", "äpärä", "puta ka", "putang ina", "tang ina", "tangina", "burat", "bayag", "bobo", "nognog", "tanga", "ulol", "kantot", "anak ka ng puta", "ulol", "jakol", "baiser", "bander", "bigornette", "bite", "bitte", "bloblos", "bordel", "bourré", "bourrée", "brackmard", "branlage", "branler", "branlette", "branleur", "branleuse", "brouter le cresson", "caca", "chatte", "chiasse", "chier", "chiottes", "clito", "clitoris", "con", "connard", "connasse", "conne", "couilles", "cramouille", "cul", "déconne", "déconner", "emmerdant", "emmerder", "emmerdeur", "emmerdeuse", "enculé", "enculée", "enculeur", "enculeurs", "enfoiré", "enfoirée", "étron", "fille de pute", "fils de pute", "folle", "foutre", "gerbe", "gerber", "gouine", "grande folle", "grogniasse", "gueule", "jouir", "la putain de ta mère", "MALPT", "ménage à trois", "merde", "merdeuse", "merdeux", "meuf", "nègre", "negro", "nique ta mère", "nique ta race", "palucher", "pédale", "pédé", "péter", "pipi", "pisser", "pouffiasse", "pousse-crotte", "putain", "pute", "ramoner", "sac à foutre", "sac à merde", "salaud", "salope", "suce", "tapette", "tanche", "teuch", "tringler", "trique", "troncher", "trou du cul", "turlute", "zigounette", "zizi", "noune", "osti", "criss", "crisse", "calice", "tabarnak", "viarge", "aand", "aandu", "balatkar", "balatkari", "behen chod", "beti chod", "bhadva", "bhadve", "bhandve", "bhangi", "bhootni ke", "bhosad", "bhosadi ke", "boobe", "chakke", "chinaal", "chinki", "chod", "chodu", "chodu bhagat", "chooche", "choochi", "choope", "choot", "choot ke baal", "chootia", "chootiya", "chuche", "chuchi", "chudaap", "chudai khanaa", "chudam chudai", "chude", "chut", "chut ka chuha", "chut ka churan", "chut ka mail", "chut ke baal", "chut ke dhakkan", "chut maarli", "chutad", "chutadd", "chutan", "chutia", "chutiya", "gaand", "gaandfat", "gaandmasti", "gaandufad", "gandfattu", "gandu", "gashti", "gasti", "ghassa", "ghasti", "gucchi", "gucchu", "harami", "haramzade", "hawas", "hawas ke pujari", "hijda", "hijra", "jhant", "jhant chaatu", "jhant ka keeda", "jhant ke baal", "jhant ke pissu", "jhantu", "kamine", "kaminey", "kanjar", "kutta", "kutta kamina", "kutte ki aulad", "kutte ki jat", "kuttiya", "loda", "lodu", "lund", "lund choos", "lund ka bakkal", "lund khajoor", "lundtopi", "lundure", "maa ki chut", "maal", "madar chod", "madarchod", "madhavchod", "mooh mein le", "mutth", "mutthal", "najayaz", "najayaz aulaad", "najayaz paidaish", "paki", "pataka", "patakha", "raand", "randaap", "randi", "randi rona", "saala", "saala kutta", "saali kutti", "saali randi", "suar", "suar ke lund", "suar ki aulad", "tatte", "tatti", "teri maa ka bhosada", "teri maa ka boba chusu", "teri maa ki behenchod", "teri maa ki chut", "tharak", "tharki", "tu chuda", "balfasz", "balfaszok", "balfaszokat", "balfaszt", "barmok", "barmokat", "barmot", "barom", "baszik", "bazmeg", "buksza", "bukszák", "bukszákat", "bukszát", "búr", "búrok", "csöcs", "csöcsök", "csöcsöket", "csöcsöt", "fasz", "faszfej", "faszfejek", "faszfejeket", "faszfejet", "faszok", "faszokat", "faszt", "fing", "fingok", "fingokat", "fingot", "franc", "francok", "francokat", "francot", "geci", "gecibb", "gecik", "geciket", "gecit", "kibaszott", "kibaszottabb", "kúr", "kurafi", "kurafik", "kurafikat", "kurafit", "kurva", "kurvák", "kurvákat", "kurvát", "leggecibb", "legkibaszottabb", "legszarabb", "marha", "marhák", "marhákat", "marhát", "megdöglik", "pele", "pelék", "picsa", "picsákat", "picsát", "pina", "pinák", "pinákat", "pinát", "pofa", "pofákat", "pofát", "pöcs", "pöcsök", "pöcsöket", "pöcsöt", "punci", "puncik", "segg", "seggek", "seggeket", "segget", "seggfej", "seggfejek", "seggfejeket", "seggfejet", "szajha", "szajhák", "szajhákat", "szajhát", "szar", "szarabb", "szarik", "szarok", "szarokat", "szart", "allupato", "ammucchiata", "anale", "arrapato", "arrusa", "arruso", "assatanato", "bagascia", "bagassa", "bagnarsi", "baldracca", "balle", "battere", "battona", "belino", "biga", "bocchinara", "bocchino", "bofilo", "boiata", "bordello", "brinca", "bucaiolo", "budiùlo", "busone", "cacca", "caciocappella", "cadavere", "cagare", "cagata", "cagna", "casci", "cazzata", "cazzimma", "cazzo", "cesso", "cazzone", "checca", "chiappa", "chiavare", "chiavata", "ciospo", "ciucciami il cazzo", "coglione", "coglioni", "cornuto", "cozza", "culattina", "culattone", "culo", "ditalino", "fava", "femminuccia", "fica", "figa", "figlio di buona donna", "figlio di puttana", "figone", "finocchio", "fottere", "fottersi", "fracicone", "fregna", "frocio", "froscio", "goldone", "guardone", "imbecille", "incazzarsi", "incoglionirsi", "ingoio", "leccaculo", "lecchino", "lofare", "loffa", "loffare", "mannaggia", "merda", "merdata", "merdoso", "mignotta", "minchia", "minchione", "mona", "monta", "montare", "mussa", "nave scuola", "nerchia", "padulo", "palle", "palloso", "patacca", "patonza", "pecorina", "pesce", "picio", "pincare", "pippa", "pinnolone", "pipì", "pippone", "pirla", "pisciare", "piscio", "pisello", "pistolotto", "pomiciare", "pompa", "pompino", "porca", "porca madonna", "porca miseria", "porca puttana", "porco", "porco due", "porco zio", "potta", "puppami", "puttana", "quaglia", "recchione", "regina", "rincoglionire", "rizzarsi", "rompiballe", "rompipalle", "ruffiano", "sbattere", "sbattersi", "sborra", "sborrata", "sborrone", "sbrodolata", "scopare", "scopata", "scorreggiare", "sega", "slinguare", "slinguata", "smandrappata", "soccia", "socmel", "sorca", "spagnola", "spompinare", "sticchio", "stronza", "stronzata", "stronzo", "succhiami", "succhione", "sveltina", "sverginare", "tarzanello", "terrone", "testa di cazzo", "tette", "tirare", "topa", "troia", "trombare", "vacca", "vaffanculo", "vangare", "zinne", "zio cantante", "zoccola", "3p", "g スポット", "s ＆ m", "sm", "sm女王", "xx", "アジアのかわいい女の子", "アスホール", "アナリングス", "アナル", "いたずら", "イラマチオ", "エクスタシー", "エスコート", "エッチ", "エロティズ ", "エロティック", "オーガズム", "オカマ", "おしっこ", "おしり", "オシリ", "おしりのあな", "おっぱい", "オッパイ", "オナニー", "オマン コ", "おもらし", "お尻", "カーマスートラ", "カント", "クリトリス", "グループ・セックス", "グロ", "クンニリングス", "ゲイ・セックス", "ゲイボーイ", "ゴールデンシャワー", "コカイン", "ゴックン", "サディ ズム", "しばり", "スウィンガー", "スカートの中", "スカトロ", "スト ラップオン", "ストリップ劇場", "スラット", "スリット", "セクシーな", "セクシーな 10 代", "セックス", "ソドミー", "ちんこ", "ディープ・スロート", "ディック", "ディルド", "デートレイプ", "デブ", "テレフ ォンセックス", "ドッグスタイル", "トップレス", "なめ", "ニガー", " ヌード", "ネオ・ナチ", "ハードコア", "パイパン", "バイブレーター", "バック・スタイル", "パンティー", "ビッチ", "ファック", "ファンタジー", "フィスト", "フェティッシュ", "フェラチオ", "ふたなり", "ぶっ かけ", "フック", "プリンス アルバート ピアス", "プレイボーイ", "ベ アバック", "ペニス", "ペニスバンド", "ボーイズラブ", "ボールギャグ", "ぽっちゃり", "ホモ", "ポルノ", "ポルノグラフィー", "ボンテージ", "マザー・ファッカー", "マスターベーション", "まんこ", "やおい", " やりまん", "ラティーナ", "ラバー", "ランジェリー", "レイプ", "レズ ビアン", "ローター", "ロリータ", "淫乱", "陰毛", "革抑制", "騎上位", "巨根", "巨乳", "強姦犯", "玉なめ", "玉舐め", "緊縛", "近親相姦", "嫌い", "後背位", "合意の性交", "拷問", "殺し方", "殺人事件", "殺 人方法", "支配", "児童性虐待", "自己愛性", "射精", "手コキ", "獣姦", "女の子", "女王様", "女子高生", "女装", "新しいポルノ", "人妻", "人種", "性交", "正常位", "生殖器", "精液", "挿入", "足フェチ", "足 を広げる", "大陰唇", "脱衣", "茶色のシャワー", "中出し", "潮吹き女", "潮吹き男性", "直腸", "剃毛", "貞操帯", "奴隷", "二穴", "乳首", "尿道プレイ", "覗き", "売春婦", "縛り", "噴出", "糞", "糞尿愛好症", "糞便", "平手打ち", "変態", "勃起する", "夢精", "毛深い", "誘惑", "幼児性愛者", "裸", "裸の女性", "乱交", "両性", "両性具有", "両刀", "輪姦", "卍", "宦官", "肛門", "膣", "abbuc", "aεeṭṭuḍ", "aḥeččun", "taḥeččunt", "axuzziḍ", "asxuẓeḍ", "qqu", "qquɣ", "qqiɣ", "qqan", "qqant", "tteqqun", "tteqqunt", "tteqqun", "aqerqur", "ajeḥniḍ", "awellaq", "iwellaqen", "iḥeččan", "iḥeččunen", "uqan", "taxna", "강간", "개새끼", "개자식", "개좆", "개차반", "거유", "계집년", "고자", "근친", "노모", "니기미", "뒤질래", "딸딸이", "때씹", "또라이", "뙤놈", "로리타", "망가", "몰카", "미친", "미친새끼", "바바리맨", "변태", "병신", "보지", "불알", "빠구리", "사까시", "섹스", "스와 핑", "쌍놈", "씨발", "씨발놈", "씨팔", "씹", "씹물", "씹빨", "씹새 끼", "씹알", "씹창", "씹팔", "암캐", "애자", "야동", "야사", "야애 니", "엄창", "에로", "염병", "옘병", "유모", "육갑", "은꼴", "자위", "자지", "잡년", "종간나", "좆", "좆만", "죽일년", "쥐좆", "직촬", "짱깨", "쪽바리", "창녀", "포르노", "하드코어", "호로", "화냥년", "후레아들", "후장", "희쭈그리""aardappels afgieten", "achter het raam zitten", "afberen", "aflebberen", "afrossen", "afrukken", "aftrekken", "afwerkplaats", "afzeiken", "afzuigen", "een halve man en een paardekop", "anita", "asbak", "aso", "bagger schijten", "balen", "bedonderen", "befborstel", "beffen", "bekken", "belazeren", "besodemieterd zijn", "besodemieteren", "beurt", "boemelen", "boerelul", "boerenpummel", "bokkelul", "botergeil", "broekhoesten", "brugpieper", "buffelen", "buiten de pot piesen", "da's kloten van de bok", "de ballen", "de hoer spelen", "de hond uitlaten", "de koffer induiken", "del", "de pijp uitgaan", "dombo", "draaikont", "driehoog achter wonen", "drol", "drooggeiler", "droogkloot", "een beurt geven", "een nummertje maken", "een wip maken", "eikel", "engerd", "flamoes", "flikken", "flikker", "gadverdamme", "galbak", "gat", "gedoogzone", "geilneef", "gesodemieter", "godverdomme", "graftak", "gras maaien", "gratenkut", "greppeldel", "griet", "hoempert", "hoer", "hoerenbuurt", "hoerenloper", "hoerig", "hol", "hufter", "huisdealer", "johny", "kanen", "kettingzeug", "klaarkomen", "klerebeer", "klojo", "klooien", "klootjesvolk", "klootoog", "klootzak", "kloten", "knor", "kont", "kontneuken", "krentekakker", "kut", "kuttelikkertje", "kwakkie", "liefdesgrot", "lul", "lul-de-behanger", "lulhannes", "lummel", "mafketel", "matennaaier", "matje", "mof", "muts", "naaien", "naakt", "neuken", "neukstier", "nicht", "oetlul", "opgeilen", "opkankeren", "oprotten", "opsodemieteren", "op z'n hondjes", "op z'n sodemieter geven", "opzouten", "ouwehoer", "ouwehoeren", "ouwe rukker", "paal", "paardelul", "palen", "penoze", "piesen", "pijpbekkieg", "pijpen", "pik", "pleurislaaier", "poep", "poepen", "poot", "portiekslet", "pot", "potverdorie", "publiciteitsgeil", "raaskallen", "reet", "reetridder", "reet trappen, voor zijn", "remsporen", "reutelen", "rothoer", "rotzak", "rukhond", "rukken", "schatje", "schijt", "schijten", "schoft", "schuinsmarcheerder", "shit", "slempen", "slet", "sletterig", "slik mijn zaad", "snol", "spuiten", "standje", "standje-69", "stoephoer", "stootje", "stront", "sufferd", "tapijtnek", "teef", "temeier", "teringlijer", "toeter", "tongzoeng", "triootjeg", "trottoir prostituée", "trottoirteef", "vergallen", "verkloten", "verneuken", "viespeuk", "vingeren", "vleesroos", "voor jan lul", "voor jan-met-de-korte-achternaam", "watje", "welzijnsmafia", "wijf", "wippen", "wuftje", "zaadje", "zakkenwasser", "zeiken", "zeiker", "zuigen", "zuiplap", "asshole", "dritt", "drittsekk", "faen", "faen i helvete", "fan", "fanken", "fitte", "forbanna", "forbannet", "forjævlig", "fuck", "fy faen", "føkk", "føkka", "føkkings", "jævla", "jævlig", "helvete", "helvetet", "kuk", "kukene", "kuker", "morraknuller", "morrapuler", "nigger", "pakkis", "pikk", "pokker", "ræva", "ræven", "satan", "shit", "sinnsykt", "skitt", "sotrør", "ståpikk", "ståpikkene", "ståpikker", "svartheiteste", "burdel", "burdelmama", "chuj", "chujnia", "ciota", "cipa", "cyc", "debil", "dmuchać", "do kurwy nędzy", "dupa", "dupek", "duperele", "dziwka", "fiut", "gówno", "gówno prawda", "huj", "huj ci w dupę", "jajco", "jajko", "ja pierdolę", "jebać", "jebany", "kurwa", "kurwy", "kutafon", "kutas", "lizać pałę", "obciągać chuja", "obciągać fiuta", "obciągać loda", "pieprzyć", "pierdolec", "pierdolić", "pierdolnąć", "pierdolnięty", "pierdoła", "pierdzieć", "pizda", "pojeb", "pojebany", "popierdolony", "robic loda", "robić loda", "ruchać", "rzygać", "skurwysyn", "sraczka", "srać", "suka", "syf", "wkurwiać", "zajebisty", "aborto", "amador", "ânus", "aranha", "ariano", "balalao", "bastardo", "bicha", "biscate", "bissexual", "boceta", "boob", "bosta", "braulio de borracha", "bumbum", "burro", "cabrao", "cacete", "cagar", "camisinha", "caralho", "cerveja", "chochota", "chupar", "clitoris", "cocaína", "coito", "colhoes", "comer", "cona", "consolo", "corno", "cu", "dar o rabo", "dum raio", "esporra", "fecal", "filho da puta", "foda", "foda-se", "foder", "frango assado", "gozar", "grelho", "heroína", "heterosexual", "homem gay", "homoerótico", "homosexual", "inferno", "lésbica", "lolita", "mama", "merda", "paneleiro", "passar um cheque", "pau", "peidar", "pênis", "pinto", "porra", "puta", "puta que pariu", "puta que te pariu", "queca", "sacanagem", "saco", "torneira", "transar", "vadia", "vai-te foder", "vai tomar no cu", "veado", "vibrador", "xana", "xochota", "bychara", "byk", "chernozhopyi", "dolboy'eb", "ebalnik", "ebalo", "ebalom sch'elkat", "gol", "mudack", "opizdenet", "osto'eblo", "ostokhuitel'no", "ot'ebis", "otmudohat", "otpizdit", "otsosi", "padlo", "pedik", "perdet", "petuh", "pidar gnoinyj", "pizda", "pizdato", "pizdatyi", "piz'det", "pizdetc", "pizdoi nakryt'sja", "pizd'uk", "piz`dyulina", "podi ku'evo", "poeben", "po'imat' na konchik", "po'iti posrat", "po khuy", "poluchit pizdy", "pososi moyu konfetku", "prissat", "proebat", "promudobl'adsksya pizdopro'ebina", "propezdoloch", "prosrat", "raspeezdeyi", "raspizdatyi", "raz'yebuy", "raz'yoba", "s'ebat'sya", "shalava", "styervo", "sukin syn", "svodit posrat", "svoloch", "trakhat'sya", "trimandoblydskiy pizdoproyob", "ubl'yudok", "uboy", "u'ebitsche", "vafl'a", "vafli lovit", "v pizdu", "vyperdysh", "vzdrochennyi", "yeb vas", "za'ebat", "zaebis", "zalupa", "zalupat", "zasranetc", "zassat", "zlo'ebuchy", "бздёнок", "блядки", "блядовать", "блядство", "блядь", "бугор", "во пизду", "встать раком", "выёбываться", "гандон", "говно", "говнюк", "голый", "дать пизды", "дерьмо", "дрочить", "другой дразнится", "ёбарь", "ебать", "ебать-копать", "ебло", "ебнуть", "ёб твою мать", "жопа", "жополиз", "играть на кожаной флейте", "измудохать", "каждый дрочит как он хочет", "какая разница", "как два пальца обоссать", "курите мою трубку", "лысого в кулаке гонять", "малофья", "манда", "мандавошка", "мент", "муда", "мудило", "мудозвон", "наебать", "наебениться", "наебнуться", "на фиг", "на хуй", "на хую вертеть", "на хуя", "нахуячиться", "невебенный", "не ебет", "ни за хуй собачу", "ни хуя", "обнаженный", "обоссаться можно", "один ебётся", "опесдол", "офигеть", "охуеть", "охуительно", "половое сношение", "секс", "сиськи", "спиздить", "срать", "ссать", "траxать", "ты мне ваньку не валяй", "фига", "хапать", "хер с ней", "хер с ним", "хохол", "хрен", "хуёво", "хуёвый", "хуем груши околачивать", "хуеплет", "хуило", "хуиней страдать", "хуиня", "хуй", "хуйнуть", "хуй пинать", "arsle", "brutta", "discofitta", "dra åt helvete", "fan", "fitta", "fittig", "för helvete", "helvete", "hård", "jävlar", "knulla", "kuk", "kuksås", "kötthuvud", "köttnacke", "moona", "moonade", "moonar", "moonat", "mutta", "nigger", "neger", "olla", "pippa", "pitt", "prutt", "pök", "runka", "röv", "rövhål", "rövknulla", "satan", "skita", "skit ner dig", "skäggbiff", "snedfitta", "snefitta", "stake", "subba", "sås", "sätta på", "tusan", "กระดอ", "กระเด้า", "กระหรี่", "กะปิ", "กู", "ขี้", "ควย", "จิ๋ม", "จู๋", "เจ๊ ก", "เจี๊ยว", "ดอกทอง", "ตอแหล", "ตูด", "น้ําแตก", "มึง", "แม่ง", "เย็ด", "รูตูด", "ล้างตู้เย็น", "ส้นตีน", "สัด", "เสือก", "หญิงชาติชั่ว", "หลั่ง", "ห่า", "หํ า", "หี", "เหี้ย", "อมนกเขา", "ไอ้ควาย", "ghuy'cha'", "QI'yaH", "Qu'vatlh", "13.", "13点", "三级片", "下三烂", "下贱", "个老子的", "九游", "乳", "乳交", "乳头", "乳房", "乳波臀浪", "交配", "仆街", "他奶奶", "他奶奶的", "他奶娘的", "他妈", "他妈ㄉ王八蛋", "他妈地", "他妈的", " 他娘", "他马的", "你个傻比", "你他马的", "你全家", "你奶奶的", "你 她马的", "你妈", "你妈的", "你娘", "你娘卡好", "你娘咧", "你它妈的", "你它马的", "你是鸡", "你是鸭", "你马的", "做爱", "傻比", "傻逼", "册那", "军妓", "几八", "几叭", "几巴", "几芭", "刚度", "刚瘪三", "包皮", "十三点", "卖B", "卖比", "卖淫", "卵", "卵子", "双峰微颤", "口交", "口肯", "叫床", "吃屎", "后庭", "吹箫", "塞你公", "塞你娘", "塞你母", "塞你爸", "塞你老师", "塞你老母", "处女", "外阴", "大卵 子", "大卵泡", "大鸡巴", "奶", "奶奶的熊", "奶子", "奸", "奸你", " 她妈地", "她妈的", "她马的", "妈B", "妈个B", "妈个比", "妈个老比", "妈妈的", "妈比", "妈的", "妈的B", "妈逼", "妓", "妓女", "妓院", " 妳她妈的", "妳妈的", "妳娘的", "妳老母的", "妳马的", "姘头", "姣西", "姦", "娘个比", "娘的", "婊子", "婊子养的", "嫖娼", "嫖客", "它妈地", "它妈的", "密洞", "射你", "射精", "小乳头", "小卵子", "小卵泡", "小瘪三", "小肉粒", "小骚比", "小骚货", "小鸡巴", "小鸡鸡", "屁 ", "屁股", "屄", "屌", "巨乳", "干x娘", "干七八", "干你", "干你妈", "干你娘", "干你老母", "干你良", "干妳妈", "干妳娘", "干妳老母", "干妳马", "干您娘", "干机掰", "干死CS", "干死GM", "干死你", "干死客服", "幹", "强奸", "强奸你", "性", "性交", "性器", "性无能", "性爱", "情色", "想上你", "懆您妈", "懆您娘", "懒8", "懒八", "懒叫", "懒教", "成人", "我操你祖宗十八代", "扒光", "打炮", "打飞机", "抽插", "招 妓", "插你", "插死你", "撒尿", "操你", "操你全家", "操你奶奶", "操 你妈", "操你娘", "操你祖宗", "操你老妈", "操你老母", "操妳", "操妳 全家", "操妳妈", "操妳娘", "操妳祖宗", "操机掰", "操比", "操逼", " 放荡", "日他娘", "日你", "日你妈", "日你老娘", "日你老母", "日批", "月经", "机八", "机巴", "机机歪歪", "杂种", "浪叫", "淫", "淫乱", "淫妇", "淫棍", "淫水", "淫秽", "淫荡", "淫西", "湿透的内裤", "激情", "灨你娘", "烂货", "烂逼", "爛", "狗屁", "狗日", "狗狼养的", "玉 ", "王八蛋", "瓜娃子", "瓜婆娘", "瓜批", "瘪三", "白烂", "白痴", "白癡", "祖宗", "私服", "笨蛋", "精子", "老二", "老味", "老母", "老瘪 三", "老骚比", "老骚货", "肉壁", "肉棍子", "肉棒", "肉缝", "肏", " 肛交", "肥西", "色情", "花柳", "荡妇", "賤", "贝肉", "贱B", "贱人", "贱货", "贼你妈", "赛你老母", "赛妳阿母", "赣您娘", "轮奸", "迷药", "逼", "逼样", "野鸡", "阳具", "阳萎", "阴唇", "阴户", "阴核", "阴毛", "阴茎", "阴道", "阴部", "雞巴", "靠北", "靠母", "靠爸", "靠背", "靠腰", "驶你公", "驶你娘", "驶你母", "驶你爸", "驶你老师", "驶你老母", "骚比", "骚货", "骚逼", "鬼公", "鸡8", "鸡八", "鸡叭", "鸡 ", "鸡奸", "鸡巴", "鸡芭", "鸡鸡", "龟儿子", "龟头", "𨳒", "陰莖", "㞗", "尻", "𨳊", "鳩", "🖕", "𨶙", "撚", "𨳍", "柒", "閪", "仆街", "咸家鏟", "冚家鏟", "咸家伶", "冚家拎", "笨實", "粉腸", "屎忽", "躝癱", "你老闆", "你老味", "你老母", "硬膠"
]





class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Bu, mesaj içeriklerini okumak için gerekli
        intents.members = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f'Bot {self.user} olarak giriş yaptı.')

    async def on_message(self, message):
        if message.author == self.user or message.author.guild_permissions.administrator:
            return

        for bad_word in BAD_WORDS:
            if f" {bad_word} " in f" {message.content.lower()} ":
                await message.delete()  # Mesajı sil
                warning_message = await message.channel.send(f"{message.author.mention}, lütfen argo veya küfür kullanmayın!")
                await asyncio.sleep(4)
                await warning_message.delete()
                return

client = MyClient()
tree = client.tree

@tree.command(name='clear', description="Belirtilen sayıda mesajı siler")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, limit: int):
    await interaction.response.defer(ephemeral=True)
    await interaction.channel.purge(limit=limit + 1)  # Kullanıcının yazdığı komut mesajını da silmek için +1 ekliyoruz

    embed = discord.Embed(
        title=f"{limit} mesaj silindi.",
        description="",
        color=discord.Color.red()
    )

    confirmation = await interaction.followup.send(embed=embed)
    await asyncio.sleep(2)
    await confirmation.delete()

@tree.command(name='spam', description="Belirtilen mesajı belirtilen sayıda spamlar")
async def spam(interaction: discord.Interaction, times: int, message: str):
    await interaction.response.defer(ephemeral=True)
    
    if times > 10:  # Spam sayısını sınırlamak için
        await interaction.followup.send("En fazla 10 kere spam yapabilirsiniz!", ephemeral=True)
        return
    
    messages = []  # Gönderilen 

    for _ in range(times):
        msg = await interaction.channel.send(message)
        messages.append(msg)  # Gönderilen mesajı listeye ekle

    await asyncio.sleep(60)  # 1 dakika bekle

    # Tüm spam mesajlarını sil
    for msg in messages:
        await msg.delete()

@tree.command(name='pban', description="Belirtilen kullanıcıyı kalıcı olarak yasaklar")
@app_commands.checks.has_permissions(ban_members=True)
async def perma_ban(interaction: discord.Interaction, user: discord.Member, reason: str = "Sebep belirtilmedi."):
    await interaction.response.defer(ephemeral=True)
    
    try:
        # Kullanıcıyı DM'lerden bilgilendir
        await user.send(f"{interaction.guild.name} sunucusundan kalıcı olarak yasaklandınız. Sebep: {reason}")

        # Sunucudan kullanıcıyı yasakla
        await interaction.guild.ban(user, reason=reason)

        # Komutu kullanan kişiye bilgilendirme mesajı gönder
        await interaction.followup.send(f"{user} kalıcı olarak yasaklandı. Sebep: {reason}")

    except discord.Forbidden:
        await interaction.followup.send("Bu kullanıcıyı yasaklama yetkim yok.", ephemeral=True)
    except discord.HTTPException:
        await interaction.followup.send("Yasaklama işlemi sırasında bir hata meydana geldi.", ephemeral=True)
    except discord.NotFound:
        await interaction.followup.send("Bu kullanıcı bulunamadı.", ephemeral=True)

@tree.command(name='hosgeldin', description="Belirtilen kanala gelen yeni üyeleri hoşgeldin mesajı ile karşılar ve rol verir")
@app_commands.checks.has_permissions(manage_roles=True, manage_nicknames=True)
async def hosgeldin(interaction: discord.Interaction, kanal: discord.TextChannel, rol: discord.Role):
    await interaction.response.defer(ephemeral=True)
    
    @client.event
    async def on_member_join(member):
        # Hoşgeldin mesajı gönder
        msg = await kanal.send(f"Hoşgeldin {member.mention}!")

        # Yetki kontrolü
        bot_member = interaction.guild.me
        if not bot_member.guild_permissions.manage_roles:
            await kanal.send(f"Rol atamak için yeterli iznim yok.")
            return
        if bot_member.top_role.position <= rol.position:
            await kanal.send(f"Rol ataması için rolüm yeterli değil.")
            return
        
        # Rolü ata ve yetki kontrol et
        try:
            await member.add_roles(rol)
        except discord.Forbidden:
            await kanal.send(f"Rol ataması için yetkim yok, {member.mention}.")
            return
        except discord.HTTPException as e:
            await kanal.send(f"Rol atanırken bir hata oluştu, {member.mention}: {e}.")
            return
        
        # Toplam üye sayısını al ve kullanıcı adını güncelle
        total_members = len(member.guild.members)
        new_nick = f"C.J.N.G | {member.display_name}"
        try:
            await member.edit(nick=new_nick)
            await msg.edit(content=f"**<:login:1256592893754216458> {member.mention} Çıkageldi! Şimdi Toplam Üye Sayısı {total_members} Oldu .**")
        except discord.Forbidden:
            await msg.edit(content=f"Hoşgeldin {member.mention}! Ama adını değiştiremedim, yetkim yok.")
        except discord.HTTPException:
            await msg.edit(content=f"Hoşgeldin {member.mention}! Ama bir hata oluştu, adını değiştiremiyorum.")

@clear.error
async def clear_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.followup.send("Bu komutu kullanmak için yeterli yetkiniz yok.", ephemeral=True)

@perma_ban.error
async def perma_ban_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.followup.send("Bu komutu kullanmak için yeterli yetkiniz yok.", ephemeral=True)

@hosgeldin.error
async def hosgeldin_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.followup.send("Bu komutu kullanmak için yeterli yetkiniz yok.", ephemeral=True)
    else:
        await interaction.followup.send(f"Hata meydana geldi: {error}", ephemeral=True)

@tree.command(name='anti_kufur', description="Mesajlarda küfür, argo veya kötü sözleri algılar ve uyarı verir")
async def anti_kufur(interaction: discord.Interaction):
    await interaction.response.send_message("Anti-küfür sistemi etkinleştirildi!", ephemeral=True)

# Hata işleyici
@anti_kufur.error
async def anti_kufur_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    await interaction.followup.send(f"Hata meydana geldi: {error}", ephemeral=True)

@tree.command(name='geliş', description="Gönderilen mesaja geliş gif'i ekler")
async def alkis(interaction: discord.Interaction, title: str):
    embed = discord.Embed(
        title=f"> **`{title}`**",
        description="",
        color=discord.Color.blue()
    )
    embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNml3NWVoeXg1OXhrM2Nwazdncm5maXB1cmY3NnVjb2lqNW82YnpsZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ymZHH7Nw0UgMjOy6ID/giphy.gif")
    await interaction.response.send_message(embed=embed)

# Bot tokeninizi buraya kendi tokeninizle değiştirmeyi unutmayın
TOKEN = 'MTI1NDk0ODIwNTgyMTY5Mzk1NA.Gt8isN.feQKzb6y65QO1wQrD3eGMrarXF0xJyEUNl2fik'  # Buraya kendi bot tokeninizi ekleyin
client.run(TOKEN)