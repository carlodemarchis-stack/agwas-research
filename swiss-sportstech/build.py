import json, html, pathlib

OUT = pathlib.Path(__file__).parent

# ---------- DATA ----------
companies = [
 # name, what, town, canton, site, segment
 ("On","Running footwear and apparel; CHF 3.0bn revenue in 2025, NYSE listed, LightSpray production facility opened in Zurich in 2025","Zurich","ZH","on.com","Big two"),
 ("Sportradar","Sports and betting data, NASDAQ listed; CHF 1.2bn attributed by the report","St. Gallen","SG","sportradar.com","Big two"),
 ("AIM Sport Vision","Patented digital overlay technology for virtual advertising in sports TV","Lucerne","LU","aimsport.com","Business of sport"),
 ("uniqFEED","AI-based virtual advertising for live sports broadcasts","Zurich","ZH","uniqfeed.com","Business of sport"),
 ("KITRIS Sports","Livestream, live scoring and video analysis for youth, school, recreational and elite sport; myKITRIS app for tennis and padel courts","Dürnten","ZH","","Business of sport"),
 ("Geobrugg","High-security race-track fencing, including for Formula 1","Romanshorn","TG","geobrugg.com","Business of sport"),
 ("Swiss Timing","Sports timing technology, part of the Swatch Group, 40+ years at Olympic Games","Corgémont","BE","swisstiming.com","Business of sport"),
 ("SIUS","Electronic target systems for shooting sports, official ISSF results provider","Effretikon","ZH","sius.com","Business of sport"),
 ("Datasport","Timing and results for Swiss running and endurance sport, 1,000+ events a year","Obergerlafingen","SO","datasport.com","Business of sport"),
 ("Technis","Real-time data analytics platform for sporting events","Lausanne","VD","technis.com","Business of sport"),
 ("Wiz-Team","Event management software for the Olympic Games and Commonwealth Games","Lausanne","VD","wiz-team.com","Business of sport"),
 ("Blocksport","Web3 and blockchain fan apps and fan tokens for clubs","Zug","ZG","blocksport.io","Business of sport"),
 ("FANtium","Platform for fans to invest directly in athletes","Zug","ZG","fantium.com","Business of sport"),
 ("Fundoo","Sponsored runs and fundraising campaigns for clubs and schools; CHF 5m raised across 300 projects by 2021","St. Gallen","SG","fundoo.ch","Business of sport"),
 ("Logitech","Gaming peripherals, partner of esports teams","Lausanne","VD","logitech.com","Business of sport"),
 ("NÜSSLI","Temporary structures for sport and events; 18 Olympic Games since 1964, Big Air jump at Milano Cortina 2026","Hüttwilen","TG","nussli.com","Business of sport"),
 ("greenTEG (CORE)","Wearable core body temperature sensor for athletes","Rümlang","ZH","corebodytemp.com","Elite sport"),
 ("Dartfish","Video analysis and performance software for coaches, federations and Olympic teams","Fribourg","FR","dartfish.com","Elite sport"),
 ("Myotest","Portable biomechanical measurement devices for federations and teams","Sion","VS","myotest.com","Elite sport"),
 ("Bearmind","EPFL spin-off, helmet-integrated head impact sensors; licensing deal with Bauer Hockey for a CSA-certified helmet in 2026/27","Lausanne","VD","","Elite sport"),
 ("VitalizedX","Saliva diagnostics and biomarker analytics for athletes","Epalinges","VD","vitalizedx.ch","Elite sport"),
 ("Storz Medical","Shockwave therapy, developed for clinical use, now standard in sports medicine","Tägerwilen","TG","storzmedical.com","Elite sport"),
 ("Bleiker Precision Engineering","Precision sport rifles for ISSF and CISM shooters","Bütschwil","SG","bleiker.ch","Elite sport"),
 ("De Martin","Functional surface coatings, including for Formula 1; 250 staff across Swiss and German plants","Wängi","TG","demartin.com","Elite sport"),
 ("Humbel Gear Technology","Precision gears and drivetrains since 1928, active in motorsport and aerospace","Kradolf","TG","humbel-gears.com","Elite sport"),
 ("Kistler","Piezoelectric measurement; force plates in elite sport, also automotive testing and industrial process control","Winterthur","ZH","kistler.com","Elite sport"),
 ("BreezeLabs","Measures breathing rate through standard headphones","Zurich","ZH","breezelabs.ai","Mass participation"),
 ("Equip Sport","App-connected self-service lockers for sports equipment; 400+ stations in Europe and North America","Rolle","VD","equip.sport","Mass participation"),
 ("MUUVR","Loyalty programme for active people, rewards for tracked activity; CHF 4m pre-Series A in 2025, Sport1 shareholder","Zurich","ZH","muuvr.io","Mass participation"),
 ("Azum","Coaching platform for training and nutrition","Zurich","ZH","azum.com","Mass participation"),
 ("coachbetter","Digital coaching platform for coaches and federations","Frauenfeld","TG","coachbetter.com","Mass participation"),
 ("Running.Coach (Quevita)","AI-driven personalised running plans","Olten","SO","running.coach","Mass participation"),
 ("LeeGroup (Lee-Sport)","Locally produced protein powders and supplements, direct to consumer","Rothenburg","LU","whey-protein.ch","Mass participation"),
 ("Sponser","Sports nutrition for professional and amateur athletes","Wollerau","SZ","sponser.ch","Mass participation"),
 ("TUUS Solutions","EPFL spin-off, plant-based hydrogel platform for steady-release energy gels; Venture Kick CHF 150k in May 2026","Lausanne","VD","tuusnutrition.ch","Mass participation"),
 ("CONICA","Sports surfaces such as running tracks and artificial turf","Schaffhausen","SH","conica.com","Mass participation"),
 ("Glice","Water- and electricity-free synthetic ice rinks","Lucerne","LU","glice.com","Mass participation"),
 ("ALLEGRA","Trail-based tourism, mountain bike and hiking trail design and construction since 2003, NOMAD trail counters","Pontresina","GR","helloallegra.com","Mass participation"),
 ("BMC Switzerland","Premium road, mountain and e-bikes for UCI WorldTour teams","Grenchen","SO","bmc-switzerland.com","Mass participation"),
 ("Alder + Eisenhut","Gymnasium equipment and facility fit-out since 1891","Ebnat-Kappel","SG","alder-eisenhut.ch","Mass participation"),
 ("Stöckli","Skis, snowboards and e-bikes, hand-made in Switzerland since 1935","Malters","LU","stoeckli.ch","Mass participation"),
 ("Odlo","Base layers and outdoor apparel since 1946","Hünenberg","ZG","odlo.com","Mass participation"),
 ("HeiQ Materials","ETH spin-off, functional textile technologies","Schlieren","ZH","heiq.com","Mass participation"),
 ("X-Bionic","Sportswear with structures for body thermoregulation","Wollerau","SZ","x-bionic.com","Mass participation"),
 ("Sphery","Interactive training hardware for gyms and rehabilitation (ExerCube)","Zurich","ZH","sphery.ch","Mass participation"),
 ("Schweiter Technologies","Composite materials for racing and high-performance equipment; most demand from aerospace, transport and construction","Steinhausen","ZG","schweiter.com","Mass participation"),
]

MSI = "Maison du Sport International, Avenue de Rhodanie 54, 1007 Lausanne"
federations = [
 # name, acronym, role, town, address, site, group
 ("World Archery","WA","Archery (Olympic)","Lausanne",MSI,"worldarchery.sport","MSI"),
 ("International Canoe Federation","ICF","Canoeing (Olympic)","Lausanne",MSI,"canoeicf.com","MSI"),
 ("International Fencing Federation","FIE","Fencing (Olympic)","Lausanne",MSI,"fie.org","MSI"),
 ("International Golf Federation","IGF","Golf (Olympic)","Lausanne",MSI,"igfgolf.org","MSI"),
 ("World Rowing","FISA","Rowing (Olympic)","Lausanne",MSI,"worldrowing.com","MSI"),
 ("World Skate","WS","Roller sports, skateboarding (Olympic)","Lausanne",MSI,"worldskate.org","MSI"),
 ("International Table Tennis Federation","ITTF","Table tennis (Olympic)","Lausanne",MSI,"ittf.com","MSI"),
 ("World Triathlon","TRI","Triathlon (Olympic)","Lausanne",MSI,"triathlon.org","MSI"),
 ("International Weightlifting Federation","IWF","Weightlifting (Olympic)","Lausanne",MSI,"iwf.sport","MSI"),
 ("World Climbing","WC","Sport climbing (Olympic); registered here, operational office in Turin","Lausanne",MSI,"worldclimbing.com","MSI"),
 ("World Taekwondo","WT","Taekwondo (Olympic); Lausanne office, main HQ Seoul","Lausanne",MSI,"worldtaekwondo.org","MSI"),
 ("International Bobsleigh and Skeleton Federation","IBSF","Bobsleigh and skeleton (Olympic winter)","Lausanne",MSI,"ibsf.org","MSI"),
 ("International Ski Mountaineering Federation","ISMF","Ski mountaineering (Olympic winter from 2026)","Lausanne",MSI,"ismf-ski.com","MSI"),
 ("World Air Sports Federation","FAI","Air sports (IOC recognised)","Lausanne",MSI,"fai.org","MSI"),
 ("World Confederation of Billiards Sports","WCBS","Cue sports (IOC recognised)","Lausanne",MSI,"wcbs.sport","MSI"),
 ("World Bridge Federation","WBF","Bridge (IOC recognised)","Lausanne",MSI,"worldbridge.org","MSI"),
 ("International Chess Federation","FIDE","Chess (IOC recognised)","Lausanne",MSI,"fide.com","MSI"),
 ("World DanceSport Federation","WDSF","Dancesport (IOC recognised)","Lausanne",MSI,"worlddancesport.org","MSI"),
 ("International Federation of Muaythai Associations","IFMA","Muaythai (IOC recognised)","Lausanne",MSI,"muaythai.sport","MSI"),
 ("International Sambo Federation","FIAS","Sambo (IOC recognised)","Lausanne",MSI,"sambo.sport","MSI"),
 ("International Federation of American Football","IFAF","American football (ASOIF associate)","Lausanne",MSI,"americanfootball.sport","MSI"),
 ("International Boxing Association","IBA","Boxing (no longer IOC recognised)","Lausanne",MSI,"iba.sport","MSI"),
 ("International Bowling Federation","IBF","Bowling (IOC recognised)","Lausanne",MSI,"bowling.sport","MSI"),
 ("International Committee of Sports for the Deaf","ICSD","Deaflympics","Lausanne",MSI,"ciss.org","MSI"),
 ("International Padel Federation","IPF","Padel","Lausanne",MSI,"padelfip.com","MSI"),
 ("International School Sport Federation","ISF","School sport","Lausanne",MSI,"isfsports.org","MSI"),
 ("World Billiard Union","UMB","Carom billiards","Lausanne",MSI,"umb-carom.org","MSI"),
 ("European Cycling Union","UEC","Continental confederation","Lausanne",MSI,"uec.ch","MSI"),
 ("European Golf Association","EGA","Continental confederation","Lausanne",MSI,"ega-golf.ch","MSI"),
 ("European Bridge League","EBL","Continental confederation","Lausanne",MSI,"eurobridge.org","MSI"),
 ("Confédération Européenne de Billard","CEB","Continental confederation","Lausanne",MSI,"eurobillard.org","MSI"),
 ("Association of Summer Olympic International Federations","ASOIF","Umbrella body, Building A, 2nd floor","Lausanne",MSI,"asoif.com","MSI"),
 ("Association of IOC Recognised International Sports Federations","ARISF","Umbrella body","Lausanne",MSI,"arisf.sport","MSI"),
 ("SportAccord","","IF convention and umbrella services, Building D, 4th floor","Lausanne",MSI,"sportaccord.sport","MSI"),
 ("World Anti-Doping Agency, European office","WADA","Anti-doping (HQ Montreal)","Lausanne",MSI,"wada-ama.org","MSI"),
 ("International Federation of Sports Medicine","FIMS","Sports medicine","Lausanne",MSI,"fims.org","MSI"),
 ("International Masters Games Association","IMGA","Masters Games","Lausanne",MSI,"imga.ch","MSI"),
 ("ThinkSport","","Lausanne region sport innovation network","Lausanne",MSI,"thinksport.org","MSI"),
 ("International Olympic Committee","IOC","Olympic Movement","Lausanne","Olympic House, Route de Vidy 9, 1007 Lausanne","olympics.com","Lausanne"),
 ("Court of Arbitration for Sport","CAS","Sports arbitration","Lausanne","Palais de Beaulieu, Avenue des Bergières 10, 1004 Lausanne (moved from Château de Béthusy in 2022)","tas-cas.org","Lausanne"),
 ("International Testing Agency","ITA","Independent anti-doping","Lausanne","Avenue de Rhodanie 58, 1007 Lausanne","ita.sport","Lausanne"),
 ("World Aquatics","","Aquatics (Olympic); HQ relocating to Budapest, target 2027; foundation and Aquatics Integrity Unit stay in Lausanne","Lausanne","Chemin de Bellevue 24a/24b, 1005 Lausanne","worldaquatics.com","Lausanne"),
 ("International Federation for Equestrian Sports","FEI","Equestrian (Olympic)","Lausanne","HM King Hussein I Building, Chemin de la Joliette 8, 1006 Lausanne","fei.org","Lausanne"),
 ("World Gymnastics (formerly FIG)","","Gymnastics (Olympic); renamed December 2025","Lausanne","Avenue de la Gare 12A, 1003 Lausanne","gymnastics.sport","Lausanne"),
 ("International Hockey Federation","FIH","Field hockey (Olympic)","Lausanne","Rue du Valentin 61, 1004 Lausanne","fih.hockey","Lausanne"),
 ("International Volleyball Federation","FIVB","Volleyball (Olympic)","Lausanne","Château Les Tourelles, Chemin Edouard-Sandoz 2-4, 1006 Lausanne","fivb.com","Lausanne"),
 ("International Skating Union","ISU","Skating (Olympic winter); new Home of Skating HQ opened October 2025","Lausanne","Chemin de Brillancourt 4, 1006 Lausanne (previously Avenue Juste-Olivier 17)","isu.org","Lausanne"),
 ("International University Sports Federation","FISU","University sport","Lausanne","Synathlon, Quartier UNIL-Centre, 1015 Lausanne","fisu.net","Lausanne"),
 ("European Athletics","EA","Continental association","Lausanne","Avenue Louis-Ruchonnet 16, 1003 Lausanne","european-athletics.com","Lausanne"),
 ("International World Games Association","IWGA","The World Games","Lausanne","Lausanne","theworldgames.org","Lausanne"),
 ("Winter Olympic Federations (formerly AIOWF)","WOF","Umbrella body","Lausanne","Lausanne","olympics.com","Lausanne"),
 ("International Judo Federation","IJF","Judo (Olympic); Lausanne seat, head office Budapest","Lausanne","Lausanne (registered seat)","ijf.org","Lausanne"),
 ("International Wushu Federation","IWUF","Wushu (IOC recognised); operations in Beijing","Lausanne","Lausanne (registered seat)","iwuf.org","Lausanne"),
 ("International Waterski and Wakeboard Federation","IWWF","Water skiing (IOC recognised)","Lausanne","Lausanne (registered seat)","iwwf.sport","Lausanne"),
 ("World Boxing","WB","Boxing (ASOIF associate, IOC provisional recognition)","Lausanne","Lausanne (registered seat)","worldboxing.org","Lausanne"),
 ("UEFA","","European football","Nyon","Route de Genève 46, 1260 Nyon","uefa.com","Vaud"),
 ("European Aquatics (formerly LEN)","","Continental confederation; agreement signed January 2026 to move HQ to Belgrade","Nyon","Nyon","european-aquatics.org","Vaud"),
 ("Union Cycliste Internationale","UCI","Cycling (Olympic), with the World Cycling Centre velodrome","Aigle","Chemin de la Mêlée 12, 1860 Aigle","uci.org","Vaud"),
 ("International Basketball Federation","FIBA","Basketball (Olympic); Patrick Baumann House of Basketball","Mies","Chemin de la FIBA 1 (formerly Route Suisse 5), 1295 Mies","fiba.basketball","Vaud"),
 ("Fédération Internationale de Motocyclisme","FIM","Motorcycling (IOC recognised); new HQ opened October 2024","Mies","Route de Suisse 11, 1295 Mies","fim-moto.com","Vaud"),
 ("World Baseball Softball Confederation","WBSC","Baseball and softball","Pully","Avenue Général-Guisan 45, 1009 Pully","wbsc.org","Vaud"),
 ("United World Wrestling","UWW","Wrestling (Olympic)","Corsier-sur-Vevey","Rue du Château 6, 1804 Corsier-sur-Vevey","uww.org","Vaud"),
 ("FIFA","","Football (Olympic)","Zurich","FIFA-Strasse 20, 8044 Zurich","fifa.com","Rest of Switzerland"),
 ("International Ice Hockey Federation","IIHF","Ice hockey (Olympic winter)","Zurich","Brandschenkestrasse 50, 8002 Zurich","iihf.com","Rest of Switzerland"),
 ("International Handball Federation","IHF","Handball (Olympic); new IHF House opened 7 May 2026 near the old town","Basel","Basel (previous address Peter Merian-Strasse 23; confirm the new one)","ihf.info","Rest of Switzerland"),
 ("International Ski and Snowboard Federation","FIS","Skiing and snowboarding (Olympic winter)","Oberhofen","Marc Hodler House, Blochstrasse 2, 3653 Oberhofen am Thunersee","fis-ski.com","Rest of Switzerland"),
 ("International Climbing and Mountaineering Federation","UIAA","Mountaineering (IOC recognised)","Bern","c/o Swiss Alpine Club, Monbijoustrasse 61, 3007 Bern","theuiaa.org","Rest of Switzerland"),
]

entities = [
 # name, role, town, address, site, group
 ("Swiss Olympic","National Olympic committee, umbrella body for 81 federations, publisher of the report; runs the Swiss Olympic Innovation Hub","Ittigen","Haus des Sports, Talgut-Zentrum 27, 3063 Ittigen","swissolympic.ch","National bodies and leagues"),
 ("Swiss Football Association (SFV/ASF)","Governs football; quoted in the report on its dependence on foreign data providers; a new Swiss Football Home in Thun announced August 2025","Muri bei Bern","Haus des Schweizer Fussballs, Worbstrasse 48, 3074 Muri bei Bern","football.ch","National bodies and leagues"),
 ("Swiss Football League (SFL)","Runs the Super League and Challenge League, 20 clubs","Bern","Maulbeerstrasse 10, 3011 Bern","sfl.ch","National bodies and leagues"),
 ("Swiss Ice Hockey Federation (SIHF)","Governs ice hockey; the National League and Swiss League run from the same address","Glattbrugg","Flughofstrasse 50, 8152 Glattbrugg","sihf.ch","National bodies and leagues"),
 ("Swiss-Ski","Governs skiing and snowboarding; host federation for the 2027 Alpine World Championships in Crans-Montana","Muri bei Bern","Muri bei Bern","swiss-ski.ch","National bodies and leagues"),
 ("Swiss Tennis","Governs tennis, national centre in Biel","Biel/Bienne","Biel/Bienne","swisstennis.ch","National bodies and leagues"),
 ("Swiss Athletics","Governs athletics","Ittigen","Haus des Sports, Ittigen","swiss-athletics.ch","National bodies and leagues"),
 ("Swiss Cycling","Governs cycling","Grenchen","Grenchen","swiss-cycling.ch","National bodies and leagues"),
 ("Federal Office of Sport (BASPO/OFSPO)","Federal sport agency, national training centre, home of the EHSM sport university","Magglingen","Hauptstrasse 247, 2532 Magglingen","baspo.admin.ch","National bodies and leagues"),
 ("Swiss Sport Integrity","National anti-doping and ethics body","Bern","Bern","sportintegrity.ch","National bodies and leagues"),
 ("Switzerland 2038","Association preparing the Winter Games bid, founded 2023 by the winter sports federations, Swiss Olympic and Swiss Paralympic","Ittigen","Ittigen","switzerland2038.ch","National bodies and leagues"),
 ("Weltklasse Zürich","Diamond League athletics meeting, Letzigrund","Zurich","","weltklassezuerich.ch","Events"),
 ("Athletissima","Diamond League athletics meeting, Stade de la Pontaise","Lausanne","","athletissima.ch","Events"),
 ("Lauberhorn races","FIS Alpine World Cup, the longest downhill on the circuit","Wengen","","lauberhorn.ch","Events"),
 ("Spengler Cup","Invitational club ice hockey tournament since 1923, owned by HC Davos","Davos","","spenglercup.ch","Events"),
 ("Tour de Suisse","UCI WorldTour stage race, run by Cycling Unlimited","Zurich","","tourdesuisse.ch","Events"),
 ("Swiss Indoors Basel","ATP 500 tennis tournament, St. Jakobshalle","Basel","","swissindoorsbasel.ch","Events"),
 ("Omega European Masters","DP World Tour golf","Crans-Montana","","omegaeuropeanmasters.com","Events"),
 ("Gonet Geneva Open","ATP 250 tennis tournament","Geneva","","genevaopen.com","Events"),
 ("EFG Swiss Open Gstaad","ATP 250 tennis tournament","Gstaad","","swissopengstaad.ch","Events"),
 ("Engadin Skimarathon","Mass participation cross-country ski race, around 14,000 starters","Maloja to S-chanf","","engadin-skimarathon.ch","Events"),
 ("Olympic Museum","IOC museum and events venue","Lausanne","Quai d'Ouchy 1, 1006 Lausanne","olympics.com/museum","Events"),
 ("SRG SSR","Public broadcaster, holds most national-team and Olympic rights; SRF in Zurich, RTS in Geneva, RSI in Lugano","Bern","Giacomettistrasse 1, 3000 Bern","srgssr.ch","Media and betting"),
 ("blue Sport (Swisscom)","Pay-TV sports channel, Swiss football rights","Zurich","","blue.ch","Media and betting"),
 ("MySports (Sunrise)","Pay-TV sports channel, National League ice hockey rights","Zurich","","mysports.ch","Media and betting"),
 ("Ringier (Blick)","Largest private media group, Blick sport desk; past joint ventures with Infront","Zurich","","ringier.com","Media and betting"),
 ("CH Media","Private TV (3+, TV24) and regional press, carries some sport","Aarau and Zurich","","chmedia.ch","Media and betting"),
 ("Keystone-SDA","National news and photo agency, supplied the images in the report","Bern","","keystone-sda.ch","Media and betting"),
 ("Swisslos","Licensed lottery and sports betting operator (Sporttip) for German-speaking Switzerland and Ticino, buyer of data and streaming","Basel","","swisslos.ch","Media and betting"),
 ("Loterie Romande","Licensed lottery and sports betting operator (Jouez Sport) for French-speaking Switzerland","Lausanne","","loro.ch","Media and betting"),
 ("Infront Sports & Media","Largest sports marketing company headquartered in Switzerland: media and marketing rights for 200+ events and federations, 1,000+ staff, owned by Wanda; co-funded the report","Zug","Grafenauweg 2, 6302 Zug","infront.sport","Agencies"),
 ("Host Broadcast Services (HBS)","Host broadcaster of the FIFA World Cup and other events, Infront subsidiary","Zug","Grafenauweg 2, 6304 Zug","hbs.tv","Agencies"),
 ("FIBA Marketing","FIBA's commercial arm, run with Infront from the same building","Zug","Grafenauweg 2, 6304 Zug","fiba.basketball","Agencies"),
 ("TEAM Marketing","Full-service agency, commercial partner of UEFA for the Champions League and Europa League since 1992; mandate runs to 2027, after which Relevent Sports takes the global rights for 2027 to 2033","Lucerne","Alpenquai 30, 6005 Lucerne","team.ch","Agencies"),
 ("Highlight Event and Entertainment / Highlight Communications","Listed holding that owns TEAM Marketing, Sport1 and the World Boxing Super Series; markets the Eurovision Song Contest and the Vienna Philharmonic","Pratteln","Netzibodenstrasse 23b, 4133 Pratteln","hlee.ch","Agencies"),
 ("Swiss Timing and Omega Timing","Official timekeeping for the Olympic Games and many federations, part of the Swatch Group","Corgémont and Biel","","swisstiming.com","Agencies"),
 ("IOC Television and Marketing Services","The IOC's commercial company, manages TOP partners and broadcast agreements","Lausanne","","olympics.com","Agencies"),
 ("Olympic Broadcasting Services","Host broadcaster of the Olympic Games; OBS SA is registered in Lausanne, operations in Madrid","Lausanne and Madrid","","obs.tv","Agencies"),
 ("AISTS","International Academy of Sport Science and Technology, master's programme and applied research, founded by the IOC and the Lausanne universities","Lausanne","Synathlon, 1015 Lausanne","aists.org","Agencies"),
 ("Lausanne Olympic Capital Foundation","Promotes Lausanne to federations and sports companies, co-funded the report","Lausanne","","olympiccapital.ch","Agencies"),
 ("SpArk","Sport innovation campus in Valais, named in the report","Sion","","sparklab.ch","Agencies"),
 ("OYM","On Your Marks, private elite training and sports science centre, named in the report's ecosystem map","Cham","","oym.ch","Agencies"),
]

data = {
 "title":"Swiss sportstech and sport governance: the directory",
 "edition":"November 2026",
 "publisher":"A Guy With A Scarf",
 "url":"https://research.aguywithascarf.com/swiss-sportstech/",
 "licence":"CC BY 4.0, cite the page",
 "companies":[dict(zip(["name","what","town","canton","site","segment"],c)) for c in companies],
 "federations":[dict(zip(["name","acronym","role","town","address","site","group"],f)) for f in federations],
 "entities":[dict(zip(["name","role","town","address","site","group"],e)) for e in entities],
}
(OUT/"data.json").write_text(json.dumps(data,ensure_ascii=False,indent=1))

# ---------- MAP ----------
import math
MAP=json.load(open("map.json"))
TOWN_KEY={"Aarau and Zurich":"Zurich","Corgémont and Biel":"Corgémont","Lausanne and Madrid":"Lausanne","Maloja to S-chanf":"Engadin"}
TOWN_CANTON={"Aigle":"VD","Basel":"BS","Bern":"BE","Biel/Bienne":"BE","Bütschwil":"SG","Cham":"ZG","Corgémont":"BE","Corsier-sur-Vevey":"VD","Crans-Montana":"VS","Davos":"GR","Dürnten":"ZH","Ebnat-Kappel":"SG","Effretikon":"ZH","Epalinges":"VD","Frauenfeld":"TG","Fribourg":"FR","Geneva":"GE","Glattbrugg":"ZH","Grenchen":"SO","Gstaad":"BE","Hünenberg":"ZG","Hüttwilen":"TG","Ittigen":"BE","Kradolf":"TG","Lausanne":"VD","Lucerne":"LU","Magglingen":"BE","Engadin":"GR","Malters":"LU","Mies":"VD","Muri bei Bern":"BE","Nyon":"VD","Obergerlafingen":"SO","Oberhofen":"BE","Olten":"SO","Pontresina":"GR","Pratteln":"BL","Pully":"VD","Rolle":"VD","Romanshorn":"TG","Rothenburg":"LU","Rümlang":"ZH","Schaffhausen":"SH","Schlieren":"ZH","Sion":"VS","St. Gallen":"SG","Steinhausen":"ZG","Tägerwilen":"TG","Wengen":"BE","Winterthur":"ZH","Wollerau":"SZ","Wängi":"TG","Zug":"ZG","Zurich":"ZH"}
CANTON_NAME={"ZH":"Zurich","BE":"Bern","LU":"Lucerne","UR":"Uri","SZ":"Schwyz","OW":"Obwalden","NW":"Nidwalden","GL":"Glarus","ZG":"Zug","FR":"Fribourg","SO":"Solothurn","BS":"Basel-Stadt","BL":"Basel-Landschaft","SH":"Schaffhausen","AR":"Appenzell Ausserrhoden","AI":"Appenzell Innerrhoden","SG":"St. Gallen","GR":"Graubünden","AG":"Aargau","TG":"Thurgau","TI":"Ticino","VD":"Vaud","VS":"Valais","NE":"Neuchâtel","GE":"Geneva","JU":"Jura"}
# Swiss SportsTech Report 2026, p.12: companies by canton of headquarters (402 in total)
REPORT_COUNT={"ZH":96,"VD":77,"BE":34,"LU":25,"SG":23,"VS":17,"ZG":17,"GR":16,"TG":12,"GE":11,"AG":9,"SO":9,"FR":8,"SZ":8,"TI":7,"BS":6,"SH":6,"NE":4,"BL":3,"GL":3,"OW":3,"AI":2,"AR":2,"NW":2,"JU":1,"UR":1}
assert sum(REPORT_COUNT.values())==402
def town_key(t): return TOWN_KEY.get(t,t)
def canton_of(t): return TOWN_CANTON.get(town_key(t),"")
def fill_class(n):
    return "f4" if n>=40 else "f3" if n>=20 else "f2" if n>=10 else "f1" if n>=5 else "f0"

def build_map():
    W,H=MAP["w"],MAP["h"]
    out=[f'<svg class="chmap" viewBox="0 0 {W} {H}" role="img" aria-labelledby="maptitle" xmlns="http://www.w3.org/2000/svg">']
    out.append('<title id="maptitle">Switzerland by canton: companies counted by the Swiss SportsTech Report 2026, with the directory entries placed on their towns</title>')
    out.append('<g class="cantons">')
    for c in MAP["cantons"]:
        n=REPORT_COUNT[c["code"]]
        out.append(f'<path class="ct {fill_class(n)}" data-c="{c["code"]}" d="{c["d"]}"><title>{CANTON_NAME[c["code"]]}: {n} companies in the report</title></path>')
    out.append('</g>')
    out.append(f'<path class="lakes" d="{MAP["lakes"]}"/>')
    # labels: count for cantons with 8 or more
    out.append('<g class="lab">')
    nudge={"ZH":(22,-20),"BE":(-8,10),"VD":(-34,-34),"GR":(0,6),"VS":(6,8),"TG":(0,-2),"SG":(4,8),"LU":(-6,6),"ZG":(14,-8),"GE":(-16,12),"FR":(-4,10),"SO":(-6,-4),"AG":(0,0),"SZ":(0,0)}
    for c in MAP["cantons"]:
        n=REPORT_COUNT[c["code"]]
        if n<8: continue
        dx,dy=nudge.get(c["code"],(0,0))
        cls=' class="dark"' if n>=40 else ''
        out.append(f'<text{cls} x="{c["cx"]+dx}" y="{c["cy"]+dy}" text-anchor="middle">{n}</text>')
    out.append('</g>')
    # entries as dots, grouped by town, sunflower layout
    groups={}
    for n,w,t,ca,s,_ in companies: groups.setdefault(town_key(t),[]).append(("co",n))
    for n,a,r,t,ad,s,_ in federations: groups.setdefault(town_key(t),[]).append(("fe",n))
    for n,r,t,ad,s,_ in entities: groups.setdefault(town_key(t),[]).append(("en",n))
    out.append('<g class="dots">')
    order={"fe":0,"en":1,"co":2}
    for town,items in groups.items():
        if town not in MAP["towns"]: continue
        x0,y0=MAP["towns"][town]
        items.sort(key=lambda i:order[i[0]])
        for i,(kind,name) in enumerate(items):
            r=3.4*math.sqrt(i); th=i*2.399963
            x=round(x0+r*math.cos(th),1); y=round(y0+r*math.sin(th),1)
            out.append(f'<circle class="{kind}" cx="{x}" cy="{y}" r="2.7" data-n="{esc(name)}"><title>{esc(name)} · {esc(town)}</title></circle>')
    out.append('</g></svg>')
    return "\n".join(out)

def canton_table():
    items=sorted(REPORT_COUNT.items(), key=lambda kv:-kv[1])
    return " · ".join(f'<button type="button" class="cb" data-c="{k}"><b>{k}</b> {v}</button>' for k,v in items)

# ---------- HTML ----------
def esc(s): return html.escape(s or "")
def site(s):
    if not s: return '<span class="na">not confirmed</span>'
    return f'<a href="https://{esc(s)}" target="_blank" rel="noopener">{esc(s)}</a>'

def table_companies(seg):
    rows=[c for c in companies if c[5]==seg]
    out=['<table class="db"><thead><tr><th>Company</th><th>What they do</th><th>Town</th><th>Canton</th><th>Website</th></tr></thead><tbody>']
    for n,w,t,ca,s,_ in rows:
        out.append(f'<tr data-c="{canton_of(t)}" data-k="{esc((n+" "+w+" "+t+" "+ca).lower())}"><td class="n" data-l="">{esc(n)}</td><td data-l="">{esc(w)}</td><td data-l="Town">{esc(t)}</td><td data-l="Canton">{esc(ca)}</td><td data-l="Web">{site(s)}</td></tr>')
    out.append('</tbody></table>'); return "\n".join(out)

def table_feds(group, with_addr=True):
    rows=[f for f in federations if f[6]==group]
    head='<th>Organisation</th><th>Acronym</th><th>Sport or role</th>'+('<th>Address</th>' if with_addr else '')+'<th>Website</th>'
    out=[f'<table class="db"><thead><tr>{head}</tr></thead><tbody>']
    for n,a,r,t,ad,s,_ in rows:
        addr=f'<td data-l="Address">{esc(ad)}</td>' if with_addr else ''
        out.append(f'<tr data-c="{canton_of(t)}" data-k="{esc((n+" "+a+" "+r+" "+t+" "+ad).lower())}"><td class="n" data-l="">{esc(n)}</td><td data-l="">{esc(a)}</td><td data-l="">{esc(r)}</td>{addr}<td data-l="Web">{site(s)}</td></tr>')
    out.append('</tbody></table>'); return "\n".join(out)

def table_ents(group):
    rows=[e for e in entities if e[5]==group]
    out=['<table class="db"><thead><tr><th>Organisation</th><th>Role</th><th>Where</th><th>Website</th></tr></thead><tbody>']
    for n,r,t,ad,s,_ in rows:
        where=esc(ad) if ad else esc(t)
        out.append(f'<tr data-c="{canton_of(t)}" data-k="{esc((n+" "+r+" "+t+" "+ad).lower())}"><td class="n" data-l="">{esc(n)}</td><td data-l="">{esc(r)}</td><td data-l="Where">{where}</td><td data-l="Web">{site(s)}</td></tr>')
    out.append('</tbody></table>'); return "\n".join(out)

ICON="data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2032%2032%22%3E%3Crect%20width%3D%2232%22%20height%3D%2232%22%20rx%3D%226%22%20fill%3D%22%231C1B19%22%2F%3E%3Crect%20x%3D%226%22%20%20y%3D%229%22%20%20width%3D%224%22%20height%3D%2214%22%20rx%3D%221%22%20fill%3D%22%23E2DED6%22%2F%3E%3Crect%20x%3D%2212%22%20y%3D%229%22%20%20width%3D%224%22%20height%3D%2214%22%20rx%3D%221%22%20fill%3D%22%23F6CFA8%22%2F%3E%3Crect%20x%3D%2218%22%20y%3D%229%22%20%20width%3D%224%22%20height%3D%2214%22%20rx%3D%221%22%20fill%3D%22%23EE9A55%22%2F%3E%3Crect%20x%3D%2224%22%20y%3D%229%22%20%20width%3D%224%22%20height%3D%2214%22%20rx%3D%221%22%20fill%3D%22%23C25C06%22%2F%3E%3C%2Fsvg%3E"
DESC="Swiss sportstech companies, every international sports federation based in Switzerland with its address, and the national bodies, events, broadcasters and agencies around them. A working directory for the Swiss SportsTech Report 2026."
TITLE="Swiss sportstech and sport governance: the directory"

nC=len(companies); nF=len(federations); nE=len(entities)

page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<link rel="canonical" href="https://research.aguywithascarf.com/swiss-sportstech/">
<meta name="description" content="{esc(DESC)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="A Guy With A Scarf: Research">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{esc(DESC)}">
<meta property="og:url" content="https://research.aguywithascarf.com/swiss-sportstech/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{esc(DESC)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="theme-color" content="#1C1B19">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Archivo+Narrow:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{color-scheme:light;--ground:#FBFAF7;--ink:#1C1B19;--slate:#5B6169;--rule:#E2DFD8;--granata:#B05708;--fill:#E9740F;--card:#fff}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--ground);color:var(--ink);font-family:"Archivo",system-ui,sans-serif;font-size:15px;line-height:1.5;font-variant-numeric:tabular-nums}}
.wrap{{max-width:1180px;margin:0 auto;padding:40px 24px 80px}}
.col{{max-width:760px}}
.crumb{{font-family:"Archivo Narrow",sans-serif;font-size:13px;letter-spacing:.03em;color:var(--slate);margin:0 0 22px}}
.crumb a{{color:var(--slate);text-decoration:none}}.crumb a:hover{{color:var(--granata)}}.crumb span{{margin:0 8px;color:#B8B3AA}}
.kicker{{font-family:"Archivo Narrow",sans-serif;font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--granata);margin:0 0 6px}}.kicker a{{color:inherit;text-decoration:none}}.kicker a:hover{{text-decoration:underline}}
h1{{font-size:clamp(25px,3.5vw,37px);font-weight:700;letter-spacing:-.022em;line-height:1.1;margin:0 0 14px;max-width:24ch;text-wrap:balance}}
p.lede{{margin:0 0 20px;max-width:68ch;color:var(--slate);font-size:16px}}
.version{{margin:0 0 22px;font-family:"Archivo Narrow",sans-serif;font-size:12px;letter-spacing:.04em;color:#A8A29A}}
.strip{{display:flex;gap:1px;height:54px;margin:0 0 10px}}
.strip span{{flex:1 1 0;border-radius:1px}}
.s0{{background:#E2DED6}}.s1{{background:#F6CFA8}}.s2{{background:#EE9A55}}.s3{{background:#C25C06}}
.striplab{{display:flex;flex-wrap:wrap;gap:18px;margin:0 0 28px;font-family:"Archivo Narrow",sans-serif;font-size:13px;color:var(--slate)}}
.striplab i{{display:inline-block;width:11px;height:11px;margin-right:6px;border-radius:1px;vertical-align:-1px;font-style:normal}}
.method{{background:#F4F1EA;border-radius:3px;padding:24px 26px 22px;margin:4px 0 6px;max-width:760px}}
.method h2{{font-size:19px;font-weight:700;letter-spacing:-.012em;margin:0 0 12px;color:var(--ink)}}
.method p{{margin:0 0 11px;font-size:13.5px;line-height:1.62;color:#5B5850}}
.method p:last-child{{margin-bottom:0}}
.mapbox{{margin:30px 0 8px;max-width:760px}}
.mapbox h2{{font-size:19px;font-weight:700;letter-spacing:-.012em;margin:0 0 6px}}
.mapbox p.cap{{margin:0 0 14px;font-size:13.5px;line-height:1.6;color:var(--slate);max-width:72ch}}
svg.chmap{{display:block;width:100%;height:auto;background:#fff;border:1px solid var(--rule);border-radius:3px}}
.ct{{stroke:#FBFAF7;stroke-width:1;cursor:pointer;transition:filter .15s}}
.ct:hover{{filter:brightness(.93)}}
.ct.on{{stroke:var(--ink);stroke-width:1.6}}
.f0{{fill:#EFEBE3}}.f1{{fill:#F6DFC6}}.f2{{fill:#F0BE8E}}.f3{{fill:#E9955A}}.f4{{fill:#C25C06}}
.lakes{{fill:#D8E1E6;pointer-events:none}}
.lab text{{font-family:"Archivo Narrow",sans-serif;font-size:14px;font-weight:700;fill:var(--ink);pointer-events:none}}
.lab text.dark{{fill:#fff}}
.dots circle{{stroke:#fff;stroke-width:.8;cursor:pointer}}
.dots .co{{fill:var(--granata)}}.dots .fe{{fill:var(--ink)}}.dots .en{{fill:var(--slate)}}
.dots circle:hover{{r:4.2}}
.maplegend{{display:flex;flex-wrap:wrap;gap:10px 18px;margin:12px 0 0;font-family:"Archivo Narrow",sans-serif;font-size:13px;color:var(--slate);align-items:center}}
.maplegend i{{display:inline-block;width:11px;height:11px;margin-right:6px;border-radius:50%;vertical-align:-1px}}
.maplegend i.sq{{border-radius:1px}}
.maplegend .gap{{flex-basis:100%;height:0}}
.cantons-all{{margin:12px 0 0;font-family:"Archivo Narrow",sans-serif;font-size:13px;line-height:2;color:var(--slate)}}
.cb{{font:inherit;border:0;background:none;padding:0 2px;color:var(--slate);cursor:pointer;border-radius:2px}}
.cb b{{color:var(--ink);font-weight:600}}
.cb:hover,.cb.on{{background:#FDF0E2;color:var(--granata)}}.cb.on b{{color:var(--granata)}}
.jump{{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 26px}}
.jump a{{font-family:"Archivo Narrow",sans-serif;font-size:13px;font-weight:600;letter-spacing:.03em;text-decoration:none;color:var(--ink);border:1px solid var(--rule);border-radius:2px;padding:7px 13px;background:#fff}}
.jump a:hover{{border-color:var(--granata);color:var(--granata)}}
.jump a::after{{content:" \\2193";color:var(--slate)}}
.controls{{background:#FDF0E2;border:1px solid #F2D6B8;border-radius:3px;padding:12px 16px;margin:8px 0 0;position:sticky;top:0;z-index:10}}
.controls.stuck{{box-shadow:0 6px 16px rgba(120,80,30,.10)}}
.row{{display:flex;flex-wrap:wrap;gap:12px 18px;align-items:center}}
input[type=search]{{font-family:"Archivo",sans-serif;font-size:14px;padding:7px 11px;border:1px solid #E7C9A6;border-radius:2px;background:#fff;min-width:240px;flex:1 1 260px;color:var(--ink)}}
input[type=search]:focus-visible{{outline:2px solid var(--granata);outline-offset:1px}}
.count{{font-family:"Archivo Narrow",sans-serif;font-size:13px;color:#8A6A4A;white-space:nowrap}}
#reset{{font-family:"Archivo Narrow",sans-serif;font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border:1px solid #E7C9A6;background:#fff;color:var(--ink);padding:7px 11px;border-radius:2px;cursor:pointer}}
#reset:hover{{border-color:var(--granata);color:var(--granata)}}
section.tier{{padding:46px 0 6px;border-top:2px solid var(--ink);margin-top:40px}}
section.tier h2{{font-size:clamp(21px,2.6vw,27px);font-weight:700;letter-spacing:-.018em;margin:0 0 8px}}
section.tier>p{{margin:0 0 6px;max-width:72ch;color:var(--slate)}}
h3.sub{{font-family:"Archivo Narrow",sans-serif;font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--granata);margin:34px 0 10px}}
h3.sub small{{font-weight:500;letter-spacing:.03em;text-transform:none;color:#9A958B;margin-left:8px}}
table.db{{width:100%;border-collapse:collapse;font-size:13.5px;line-height:1.45;background:var(--card);border:1px solid var(--rule);border-radius:3px;overflow:hidden}}
table.db th{{text-align:left;font-family:"Archivo Narrow",sans-serif;font-size:12px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:#8C877E;padding:10px 12px;border-bottom:1px solid var(--rule);background:#F7F4EE}}
table.db td{{padding:10px 12px;border-bottom:1px solid var(--rule);vertical-align:top}}
table.db tbody tr:last-child td{{border-bottom:0}}
table.db td.n{{font-weight:600;white-space:nowrap}}
table.db a{{color:var(--granata);text-decoration:none;white-space:nowrap}}
table.db a:hover{{text-decoration:underline}}
.na{{color:#B8B3AA;font-style:italic}}
tr.hide,table.db tr.hide{{display:none!important}}
.msi{{background:#FDF0E2;border:1px solid #F2D6B8;border-radius:3px;padding:14px 16px;margin:0 0 14px;font-size:13.5px;color:#5B5850;max-width:76ch}}
.msi b{{color:var(--ink)}}
.note{{margin:18px 0 0;max-width:76ch;font-size:13.5px;line-height:1.6;color:var(--slate)}}
.obs{{margin:22px 0 0;padding:18px 20px;border-left:3px solid var(--fill);background:var(--card);border-radius:3px;max-width:76ch;font-size:14px;line-height:1.6}}
.alsonote{{margin:56px 0 0;padding-top:26px;border-top:1px solid var(--rule);max-width:78ch;font-size:13.5px;line-height:1.6;color:var(--slate)}}
.src{{margin:14px 0 0;padding:0 0 0 18px;font-size:13px;line-height:1.6;color:var(--slate)}}
.src a{{color:var(--granata);text-decoration:none;word-break:break-all}}.src a:hover{{text-decoration:underline}}
.rail{{display:flex;flex-wrap:wrap;gap:16px;margin:48px 0 0}}
.promo{{background:var(--card);border:1px solid var(--rule);border-radius:3px;padding:16px 17px;flex:1 1 260px}}
.promo .eyebrow{{font-family:"Archivo Narrow",sans-serif;font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--granata);margin:0 0 7px}}
.promo h4{{font-size:16px;font-weight:700;letter-spacing:-.01em;margin:0 0 7px;line-height:1.25}}
.promo p{{margin:0 0 12px;font-size:13.5px;line-height:1.5;color:var(--slate)}}
.promo a.cta{{display:inline-block;font-family:"Archivo Narrow",sans-serif;font-size:13px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:#fff;background:var(--granata);text-decoration:none;padding:7px 13px;border-radius:2px}}
.promo a.cta:hover{{background:#8C4506}}
.promo.li .eyebrow{{color:#0A66C2}}.promo.li a.cta{{background:#0A66C2}}.promo.li a.cta:hover{{background:#08528F}}
.promo.sub .eyebrow{{color:#FF6719}}.promo.sub a.cta{{background:#FF6719}}.promo.sub a.cta:hover{{background:#DB5412}}
.promo.amz a.cta{{background:var(--fill)}}.promo.amz a.cta:hover{{background:#C25C06}}
#totop{{position:fixed;right:22px;bottom:22px;z-index:40;border:1px solid #E7C9A6;background:#FDF0E2;color:var(--ink);font-family:"Archivo Narrow",sans-serif;font-size:12px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;padding:10px 13px;border-radius:2px;cursor:pointer;opacity:0;pointer-events:none;transition:opacity .2s}}
#totop.show{{opacity:1;pointer-events:auto}}
footer{{margin-top:44px;padding-top:20px;border-top:1px solid var(--rule);color:var(--slate);font-size:13.5px;max-width:74ch}}
footer a{{color:var(--granata)}}
@media (max-width:760px){{
 .wrap{{padding:28px 16px 64px}}
 .controls{{margin-left:-16px;margin-right:-16px;border-radius:0;border-left:0;border-right:0}}
 table.db,table.db tbody,table.db tr,table.db td{{display:block;width:100%}}
 table.db thead{{display:none}}
 table.db tbody tr{{border-bottom:1px solid var(--rule);padding:12px 12px 10px}}
 table.db tbody tr:last-child{{border-bottom:0}}
 table.db td{{padding:2px 0;border:0}}
 table.db td.n{{white-space:normal;font-size:15px;margin-bottom:2px}}
 table.db td[data-l]:not([data-l=""])::before{{content:attr(data-l) " ";font-family:"Archivo Narrow",sans-serif;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:#9A958B;margin-right:4px}}
 .rail{{display:block}}.promo{{margin:0 0 14px}}
 .dots circle{{r:4}}.lab text{{font-size:16px}}
}}
</style>
</head>
<body>
<div class="wrap" id="top">
<div class="col">
<p class="crumb"><a href="/">Research Hub</a><span>/</span>Swiss sportstech</p>
<p class="kicker"><a href="https://aguywithascarf.com/">A Guy With A Scarf</a></p>
<h1>Swiss sportstech and sport governance: the directory</h1>
<p class="lede">Three lists built around the Swiss SportsTech Report 2026: the {nC} companies the report names, with segment, town and website; the {nF} international federations and sport governance bodies based in Switzerland, with street address; and the {nE} national federations, leagues, event owners, broadcasters, betting operators and agencies that make up the rest of the Swiss sports economy. Addresses checked in November 2026 against each organisation's own pages.</p>
<p class="version">Edition 1 · November 2026 · data.json alongside this page</p>

<div class="strip" aria-hidden="true">{''.join(f'<span class="s3" title="{esc(f[0])}"></span>' for f in federations if f[6]=="MSI")}{''.join(f'<span class="s2" title="{esc(f[0])}"></span>' for f in federations if f[6]=="Lausanne")}{''.join(f'<span class="s1" title="{esc(f[0])}"></span>' for f in federations if f[6]=="Vaud")}{''.join(f'<span class="s0" title="{esc(f[0])}"></span>' for f in federations if f[6]=="Rest of Switzerland")}</div>
<div class="striplab">
 <span><i class="s3"></i>One address: Maison du Sport International</span>
 <span><i class="s2"></i>Lausanne, own building or seat</span>
 <span><i class="s1"></i>Rest of Vaud</span>
 <span><i class="s0"></i>Rest of Switzerland</span>
</div>

<div class="method">
 <h2>How to read this</h2>
 <p>The company list is the illustrative sample the report itself publishes, around fifty of the 402 it mapped, chosen by the authors to show breadth rather than rank. Descriptions are condensed from the report and from the companies' own pages where the report was thin. Two websites are left blank because I could not confirm a domain.</p>
 <p>The federation list takes the wide view: Olympic and recognised federations, continental confederations, umbrella bodies and agencies. The report counts around 60, the Lausanne Olympic Capital Foundation says more than 70, and the difference is what you count. Four entries changed address or announced a move in the last twelve months and the table says which.</p>
 <p>The third list exists because the buyers a Swiss sportstech company meets first are usually a national federation, a league, an event with a broadcast contract, or one of the agencies that sell rights for all of them. Federations move more often than people assume. Check before you post a letter.</p>
</div>

<div class="mapbox" id="map">
 <h2>Where it all sits</h2>
 <p class="cap">Cantons are shaded by the number of sportstech companies the report counts there, 402 in all, with the figure shown for every canton with eight or more. The dots are the {nC+nF+nE} entries in this directory, placed on their towns. Tap a canton to filter the lists to it, tap a dot to look that entry up.</p>
 {build_map()}
 <div class="maplegend">
  <span><i class="sq" style="background:#EFEBE3"></i>under 5</span><span><i class="sq" style="background:#F6DFC6"></i>5 to 9</span><span><i class="sq" style="background:#F0BE8E"></i>10 to 19</span><span><i class="sq" style="background:#E9955A"></i>20 to 39</span><span><i class="sq" style="background:#C25C06"></i>40 and more</span>
  <span class="gap"></span>
  <span><i style="background:var(--granata)"></i>Sportstech company</span><span><i style="background:var(--ink)"></i>International federation or sport body</span><span><i style="background:var(--slate)"></i>National body, league, event, broadcaster or agency</span>
 </div>
 <p class="cantons-all">All 26 cantons, report count: {canton_table()}</p>
</div>

<nav class="jump">
 <a href="#map">Map</a>
 <a href="#companies">Companies</a>
 <a href="#federations">International federations</a>
 <a href="#national">National bodies and leagues</a>
 <a href="#events">Events</a>
 <a href="#media">Media and betting</a>
 <a href="#agencies">Agencies</a>
 <a href="#sources">Sources</a>
</nav>
</div>

<div class="controls" id="controls">
 <div class="row">
  <input type="search" id="q" placeholder="Search name, role, town, canton, address" aria-label="Search the directory">
  <button id="reset" type="button">Clear</button>
  <span class="count" id="count"></span>
 </div>
</div>

<section class="tier" id="companies">
 <h2>Part 1. Swiss sportstech companies named in the report</h2>
 <p>Grouped by the market segment the report assigns them to. A company can sit in more than one; it appears here once.</p>
 <h3 class="sub">The two that make up half the revenue</h3>
 {table_companies("Big two")}
 <h3 class="sub">Business of sport and entertainment</h3>
 {table_companies("Business of sport")}
 <h3 class="sub">Professional and elite sport</h3>
 {table_companies("Elite sport")}
 <h3 class="sub">Mass participation and active living</h3>
 {table_companies("Mass participation")}
 <p class="note">Numbers to keep next to the list, all from the report: three cantons hold about half the 402 companies, Zurich 96, Vaud 77, Bern 34, then Lucerne 25, St. Gallen 23, Valais and Zug 17 each, Graubünden 16. By technology, advanced materials 173 companies, ICT 145, sensors and devices 84, medical and biotech 58; streaming and OTT counts 15, media and broadcast 21. By market, mass participation 257, elite sport 140, business of sport 114. Garmin, registered in Schaffhausen with roughly CHF 1.9bn of fitness revenue in FY2025, sits outside the count because its strategic decisions are taken abroad.</p>
</section>

<section class="tier" id="federations">
 <h2>Part 2. International sports federations and governance bodies based in Switzerland</h2>
 <p>Grouped by where the offices are. Addresses checked against each organisation's contact page, the IOC directory or the MSI tenant list, November 2026.</p>
 <h3 class="sub">Lausanne: one address, around thirty tenants</h3>
 <div class="msi">The <b>Maison du Sport International</b>, Avenue de Rhodanie 54, 1007 Lausanne (<a href="https://www.msi-lausanne.ch" target="_blank" rel="noopener">msi-lausanne.ch</a>), opened in 2006, owned in equal parts by the City of Lausanne, the Canton of Vaud and the IOC. Everything in this table shares that address.</div>
 {table_feds("MSI", with_addr=False)}
 <h3 class="sub">Lausanne: own buildings and registered seats</h3>
 {table_feds("Lausanne")}
 <h3 class="sub">Rest of the Canton of Vaud</h3>
 {table_feds("Vaud")}
 <h3 class="sub">Rest of Switzerland</h3>
 {table_feds("Rest of Switzerland")}
 <p class="note">The exception that proves the rule: World Athletics, which I drove to more than any of the above, is in Monaco (6-8 Quai Antoine 1er, worldathletics.org), and so is the International Modern Pentathlon Union. Both are a short drive from the Swiss border and a long way from Lausanne in every other sense.</p>
</section>

<section class="tier" id="national">
 <h2>Part 3. The rest of the Swiss sports economy</h2>
 <p>National federations and leagues first, then event owners, broadcasters and betting operators, then the agencies.</p>
 <h3 class="sub">National federations, leagues and public bodies</h3>
 {table_ents("National bodies and leagues")}
 <h3 class="sub" id="events">Event owners with their own commercial and broadcast operations</h3>
 {table_ents("Events")}
 <h3 class="sub" id="media">Broadcasters, sports media and betting</h3>
 {table_ents("Media and betting")}
 <h3 class="sub" id="agencies">Sports marketing, rights, production and innovation</h3>
 {table_ents("Agencies")}
 <div class="obs">Two things stood out compiling this part. Much of the Swiss rights business sits in two postcodes, Zug and Lucerne, far from Lausanne, which says something about where the money and the governance actually meet. And the biggest Swiss agency contract of the last thirty years, TEAM's UEFA mandate, ends in 2027 in favour of a US firm, and the report does not mention it, even though it is the clearest recent example of the commercial layer the authors say Switzerland lacks.</div>
</section>

<section class="alsonote" id="sources">
 <strong>Sources.</strong> The article this directory accompanies is on <a href="https://aguywithascarf.substack.com" style="color:var(--granata)">A Guy With A Scarf</a>. Primary sources for the lists:
 <ol class="src">
  <li>Swiss SportsTech Report 2026, Swiss Olympic with PwC and generis: <a href="https://www.spiritofsport.ch/dam/jcr:3a5ce897-5f90-4c2c-8251-9ba66503cc8d/Swiss_Sports_Tech_Report_2026.18e63b327fec88ad558c7090c84834cf.pdf">spiritofsport.ch (PDF)</a></li>
  <li>Maison du Sport International tenant lists: <a href="https://www.msi-lausanne.ch/en/tenants/international-sports-federations">federations</a> and <a href="https://www.msi-lausanne.ch/en/tenants/sports-organisations">organisations</a></li>
  <li>ISU new headquarters (3 October 2025): <a href="https://www.isu.org/news/the-isu-officially-opens-the-doors-of-its-new-home-of-skating-headquarters-in-lausanne-2">isu.org</a></li>
  <li>IHF new headquarters in Basel (7 May 2026): <a href="https://www.ihf.info/media-center/news/new-home-handball-ihf-officially-opens-its-new-headquarters-basel">ihf.info</a></li>
  <li>World Aquatics headquarters and Budapest transition: <a href="https://www.worldaquatics.com/about/headquarters">worldaquatics.com</a></li>
  <li>European Aquatics agreement to move to Belgrade (26 January 2026): <a href="https://swimswam.com/?p=984168">swimswam.com</a></li>
  <li>FIBA new address, Chemin de la FIBA 1: <a href="https://about.fiba.basketball/en/news/celebrations-at-inauguration-of-new-address-for-fiba-headquarters">about.fiba.basketball</a></li>
  <li>FIM new headquarters (October 2024): <a href="https://www.totalmotorcycle.com/fim-officially-opens-its-new-headquarters">totalmotorcycle.com</a></li>
  <li>FIS contact page: <a href="https://fis-ski.com/contact">fis-ski.com</a> · UIAA office: <a href="https://www.theuiaa.org/?p=663">theuiaa.org</a> · FISU and the Synathlon: <a href="https://www.fisu.net/news/now-its-official">fisu.net</a> · European Athletics: <a href="https://trackalerts.com/?p=27964">trackalerts.com</a> · World Gymnastics: <a href="https://gymnastics.sport/site/pages/privacy.php">gymnastics.sport</a></li>
  <li>FEI, FIH, FIVB, IIHF, WBSC, ISU, ITA, UWW, ASOIF, World Archery: the IOC federation directory at olympics.com/ioc and the federations' own contact pages</li>
  <li>Infront: <a href="https://www.infront.sport/contact">infront.sport</a> · TEAM Marketing: <a href="https://team.ch/media/uploads/TEAM-Corporate-Factsheet_July2024.pdf">team.ch (PDF)</a> · Highlight on the UEFA tender: <a href="https://images.finanzen.ch/nachrichten/aktien/teams-bid-in-the-tender-process-for-the-uefa-club-competitions-for-the-2027-2033-seasons-remains-unconsidered-1034341430">finanzen.ch</a></li>
  <li>Swiss Football Association: <a href="https://inside.fifa.com/associations/SUI/organisation">inside.fifa.com</a> and the Thun move: <a href="https://www.bluewin.ch/en/sport/football/thun-new-location-for-the-association-center-li.2842616">bluewin.ch</a> · Swiss Ice Hockey Federation: <a href="https://canada-central.iihf.com/fr_ca/associations/1370/switzerland">iihf.com</a></li>
  <li>Company details beyond the report: Bearmind and Bauer (<a href="https://nsga.org/?p=17110">nsga.org</a>), Equip Sport (<a href="https://vancouver.ca/news-calendar/new-sports-equipment-lockers-roll-out-mar-2026.aspx">vancouver.ca</a>), MUUVR (<a href="https://finder.techleap.nl/news/feed/muuvr-secures-chf-4m-for-app-upgrade">techleap.nl</a>), TUUS (<a href="https://www.venturekick.ch/tuus-solutions">venturekick.ch</a>), VitalizedX (<a href="https://bioalps.org/?p=26977">bioalps.org</a>), Bleiker (<a href="https://www.iwa.info/en/exhibitors/bleiker-precision-engineering-ag-2623032">iwa.info</a>), De Martin (<a href="https://www.swissmem.ch/de/zmis/firmenportraits/unsere-mitglieder/de-martin-ag.html">swissmem.ch</a>), Humbel (<a href="https://www.hermle.de/en/industries-solutions/user-reports/detail/getting-the-ratio-right/">hermle.de</a>), fundoo (<a href="https://www.esb-online.com/fileadmin/user_upload/06_News/2021/News_August_2021/2108_Medienmitteilung_fundooExpansion.pdf">esb-online.com (PDF)</a>), KITRIS (<a href="https://onlineinfo.ch/firma/kitris-sports-ag---che-214-466-274/pdf">onlineinfo.ch</a>)</li>
  <li>Map: companies by canton of headquarters from page 12 of the report; canton and lake boundaries from the <a href="https://github.com/interactivethings/swiss-maps">swiss-maps</a> package (swisstopo data), simplified; directory entries placed on their town, grouped where several share one.</li>
 </ol>
</section>

<aside class="rail">
<div class="promo li">
 <p class="eyebrow">Follow on LinkedIn</p>
 <h4>Carlo De Marchis</h4>
 <p>Daily notes on streaming, live sport and the business of media technology.</p>
 <a class="cta" href="https://www.linkedin.com/in/carlodemarchis/" target="_blank" rel="noopener">Follow me</a>
</div>
<div class="promo sub">
 <p class="eyebrow">Substack</p>
 <h4>A Guy With A Scarf on Substack</h4>
 <p>Long-form pieces, the research behind them and datasets like this one.</p>
 <a class="cta" href="https://aguywithascarf.substack.com" target="_blank" rel="noopener">Subscribe on Substack</a>
</div>
<div class="promo amz">
 <p class="eyebrow">Book</p>
 <h4>Becoming a Better B2B Tech Vendor in Sports and Media</h4>
 <p>Ten things to consider, written up from the vendor side. How vendors pitch, and what buyers actually hear.</p>
 <a class="cta" href="https://www.amazon.it/Becoming-Better-Vendor-Sports-Media/dp/B0GP66Q1ZK/" target="_blank" rel="noopener">Get the book</a>
</div>
</aside>

<footer>Carlo De Marchis · <a href="https://aguywithascarf.substack.com">A Guy With A Scarf</a> · Directory published with the article "10 things to consider about the Swiss SportsTech Report". If you spot a wrong address or a missing body, tell me and I will fix it in the next edition.</footer>
<button id="totop" type="button" aria-label="Back to top">Top ↑</button>
</div>
<script>
(function(){{
 var q=document.getElementById('q'),reset=document.getElementById('reset'),count=document.getElementById('count');
 var rows=[].slice.call(document.querySelectorAll('table.db tbody tr'));
 var subs=[].slice.call(document.querySelectorAll('h3.sub'));
 var total=rows.length;
 var canton='';var NAMES={json.dumps(CANTON_NAME)};
 function apply(){{
  var t=q.value.trim().toLowerCase(),n=0;
  rows.forEach(function(r){{var ok=(!t||r.getAttribute('data-k').indexOf(t)>-1)&&(!canton||r.getAttribute('data-c')===canton);r.classList.toggle('hide',!ok);if(ok)n++;}});
  document.querySelectorAll('.ct,.cb').forEach(function(el){{el.classList.toggle('on',!!canton&&el.getAttribute('data-c')===canton);}});
  document.querySelectorAll('table.db').forEach(function(tb){{
   var vis=tb.querySelectorAll('tbody tr:not(.hide)').length;tb.style.display=vis?'':'none';
   var h=tb.previousElementSibling;while(h&&!h.classList.contains('sub'))h=h.previousElementSibling;
   if(h)h.style.display=vis?'':'none';
  }});
  var lab=(canton?NAMES[canton]+(t?' + "'+t+'"':''):(t?'"'+t+'"':''));
  count.textContent=lab?lab+': '+n+' of '+total+' entries':total+' entries';
 }}
 q.addEventListener('input',apply);reset.addEventListener('click',function(){{q.value='';canton='';apply();q.focus();}});
 function setCanton(c){{canton=(canton===c)?'':c;apply();var ctl=document.getElementById('controls');if(canton&&ctl.getBoundingClientRect().top<0)ctl.scrollIntoView();}}
 document.querySelectorAll('.ct,.cb').forEach(function(el){{el.addEventListener('click',function(){{setCanton(el.getAttribute('data-c'));}});}});
 document.querySelectorAll('.dots circle').forEach(function(d){{d.addEventListener('click',function(ev){{ev.stopPropagation();canton='';q.value=d.getAttribute('data-n');apply();document.getElementById('controls').scrollIntoView();}});}});
 apply();
 var c=document.getElementById('controls'),tt=document.getElementById('totop');
 window.addEventListener('scroll',function(){{
  c.classList.toggle('stuck',c.getBoundingClientRect().top<=0&&window.scrollY>200);
  tt.classList.toggle('show',window.scrollY>900);
 }},{{passive:true}});
 tt.addEventListener('click',function(){{window.scrollTo({{top:0,behavior:'smooth'}});}});
}})();
</script>
<!-- Umami --><script>try{{/[?&#]noumami\\b/.test(location.href)&&localStorage.setItem('umami.disabled','1')}}catch(e){{}}</script><script defer src="https://m.aguywithascarf.com/k.js" data-website-id="b56455b9-6873-41fd-9eda-79ffb62667f7"></script><!-- End Umami -->
</body>
</html>
'''
(OUT/"index.html").write_text(page)
print(nC,nF,nE,len(page))
