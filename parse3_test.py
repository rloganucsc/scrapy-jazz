from scrapy.selector import Selector
from Jazz.items import Album
import re

doc = """
<h2>Atlantic 1200 series (12 inch 78 rpm)</h2>
<h3><a name="1201">1201 &nbsp; John Dall/Vernon Duke - This Is My Beloved, Part 1&amp;2<!-- todo --></a></h3>
<div>no details</div>
<h3><a name="1202">1202 &nbsp; John Dall/Vernon Duke - This Is My Beloved, Part 3&amp;4<!-- todo --></a></h3>
<div>no details</div>
<h3><a name="1203">1203 &nbsp; John Dall/Vernon Duke - This Is My Beloved, Part 5&amp;6<!-- todo --></a></h3>
<div>no details</div>
<h2>Atlantic 1200 series (12 inch LP)</h2>
<h3><a name="1204">1204 &nbsp; Eva LaGallienne And Richard Waring With King Webster - Romeo And Juliet Scenes, Disc 1<!-- todo --></a></h3>
<div>no details</div>
<h3><a name="1205">1205 &nbsp; Eva LaGallienne And Richard Waring With King Webster - Romeo And Juliet Scenes, Disc 2<!-- todo --></a></h3>
<div>no details</div>
<h3><a name="als-1206">ALS 1206 &nbsp; Sidney Bechet And Muggsy Spanier - Duets</a></h3>
Muggsy Spanier (cornet) Sidney Bechet (soprano saxophone, clarinet) Carmen Mastren (guitar) Wellman Braud (bass)
<div class="date">NYC, March 28, 1940</div>
<table width="100%">
<tbody><tr><td width="15%">R2773</td><td>Four Or Five Times
</td></tr><tr><td>R2774</td><td>Sweet Lorraine
</td></tr><tr><td>R2775</td><td>Up A Lazy River
</td></tr><tr><td>R2776-1</td><td>China Boy
</td></tr></tbody></table>
same personnel
<div class="date">NYC, April 6, 1940</div>
<table width="100%">
<tbody><tr><td width="15%">R2801-1</td><td>If I Could Be With You One Hour Tonight
</td></tr><tr><td>R2802-3</td><td>That's A Plenty
</td></tr><tr><td>R2803-3</td><td>Squeeze Me
</td></tr><tr><td>R2804-2</td><td>Sweet Sue, Just You
</td></tr></tbody></table>
<h3><a name="als-1207">ALS 1207 &nbsp; Mary Powers Concert</a></h3>
Frank La Forge (piano) Mary Powers (vocals)
<div class="date">NYC, July 25, 1950</div>
<table width="100%">
<tbody><tr><td width="15%">478</td><td>The Spirit Song (Haydn)
</td></tr><tr><td>479</td><td>Ombra Mai Fu (Haendel)
</td></tr><tr><td>480</td><td>Before The Crucifix (La Forge)
</td></tr><tr><td>481</td><td>Ich Liebe Dich (Beethoven)
</td></tr><tr><td>482</td><td>Extase (Duparc)
</td></tr><tr><td>483</td><td>Les Berceaux (Faure)
</td></tr><tr><td>484</td><td>El Beso (Oubradors)
</td></tr><tr><td>485</td><td>Nebbie (Respighi)
</td></tr><tr><td>486</td><td>Traume (Wagner)
</td></tr><tr><td>487</td><td>Come Sweet Death (Bach)
</td></tr><tr><td>488</td><td>Death And The Maiden (Schubert) (Der Tod Und Das Maedchen)
</td></tr><tr><td>490</td><td>Der Erl Konig (Schubert)
</td></tr><tr><td>492</td><td>Meine Liebe Ist Gruen (Brahms)
</td></tr><tr><td>493</td><td>Der Schmidt
</td></tr><tr><td>494</td><td>Dedication
</td></tr><tr><td>495</td><td>Lullaby
</td></tr><tr><td>496</td><td>Requiescat (Cory)
</td></tr></tbody></table>
<h3><a name="als-1208">ALS 1208 &nbsp; Wilbur DeParis And His Rampart Street Ramblers</a></h3>
Sidney DeParis (trumpet, vocals) Wilbur DeParis (trombone) Omer Simeon (clarinet) Don Kirkpatrick (piano) Eddie Gibbs (banjo) Harold Jackson (bass) Freddie Moore (drums)
<div class="date">NYC, September 11, 1952</div>
<table width="100%">
<tbody><tr><td width="15%">879</td><td>Hindustan
</td></tr><tr><td>880</td><td>Shreveport Stomp
</td></tr><tr><td>882</td><td>Tres Moutarde
</td></tr><tr><td>883</td><td>When The Saints Go Marching In
</td></tr><tr><td>889</td><td>Sensation Rag
</td></tr></tbody></table>
<h3><a name="als-1209">ALS 1209 &nbsp; Jack Teagarden/Rex Stewart - Big Jazz</a></h3>
Rex Stewart (cornet) Lawrence Brown (trombone) Barney Bigard (clarinet) Billy Kyle (piano) Brick Fleagle (guitar) Wellman Braud (bass) Dave Tough (drums)
<div class="date">NYC, July 23, 1940</div>
<table width="100%">
<tbody><tr><td width="15%">76396-B | 1029</td><td>Cherry
</td></tr><tr><td>76397-A | 1032</td><td>Solid Rock
</td></tr><tr><td>76398-A | 1031</td><td>Bugle Call Rag
</td></tr><tr><td>76399-A | 1030</td><td>Diga Diga Doo
</td></tr></tbody></table>
Rex Stewart (cornet) Jack Teagarden (trombone, vocals) Barney Bigard (clarinet) Ben Webster (tenor saxophone) Billy Kyle (piano) Brick Fleagle (guitar) Billy Taylor (bass) Dave Tough (drums)
<div class="date">NYC, December 15, 1940</div>
<table width="100%">
<tbody><tr><td width="15%">R3414 | 1025</td><td>St. James Infirmary
</td></tr><tr><td>R3415 | 1028</td><td>The World Is Waiting For The Sunrise
</td></tr><tr><td>R3416 | 1027</td><td>The Big Eight Blues
</td></tr><tr><td>R3417 | 1088 | 1026</td><td>Shine
</td></tr></tbody></table>
<h3><a name="als-1210">ALS 1210 &nbsp; Charles Sherrill Plays Music From "Show Boat" And "Roberta"<!-- todo --></a></h3>
<div>no details</div>
<h3><a name="als-1211">ALS 1211 &nbsp; Charles Sherrill Plays Music From "Pal Joey" And "A Connecticut Yankee"<!-- todo --></a></h3>
<div>no details</div>
<h2>Atlantic Jazz 1200 series (12 inch LP)</h2>
<h3><a name="1212">1212 &nbsp; Shorty Rogers - The Swinging Mr. Rogers</a></h3>
Shorty Rogers (trumpet) Jimmy Giuffre (clarinet, tenor, baritone saxophone) Pete Jolly (piano) Curtis Counce (bass) Shelly Manne (drums)
<div class="date">Los Angeles, CA, March 1, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1723</td><td>Isn't It Romantic
</td></tr><tr><td>1724</td><td>Not Really The Blues
</td></tr><tr><td>1725</td><td>Martians Go Home (Martians Stay Home)
</td></tr><tr><td>1726</td><td>My Heart Stood Still
</td></tr><tr><td>1728</td><td>Oh! Play That Thing
</td></tr></tbody></table>
same personnel
<div class="date">Los Angeles, CA, March 3, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1732</td><td>Trickleydidlier
</td></tr><tr><td>1734</td><td>That's What I'm Talking About
</td></tr><tr><td>1735</td><td>Michele's Meditation
</td></tr></tbody></table>
<h3><a name="1213">1213 &nbsp; Mabel Mercer Sings Cole Porter</a></h3>
Stan Freeman, Cy Walter (piano) Frank Carroll (bass) Mabel Mercer (vocals)
<div class="date">NYC, November 7, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1347A</td><td>It's De-Lovely
</td></tr><tr><td>1348A</td><td>Use Your Imagination
</td></tr><tr><td>1349</td><td>Experiment
</td></tr><tr><td>1350</td><td>It's All Right With Me
</td></tr><tr><td>1351</td><td>Ev'ry Time We Say Goodbye
</td></tr><tr><td>1352</td><td>I Am Ashamed That Women Are So Simple
</td></tr><tr><td>1353</td><td>So In Love
</td></tr><tr><td>1354</td><td>Ours
</td></tr><tr><td>1355</td><td>Ace In The Hole
</td></tr><tr><td>1356</td><td>Looking At You
</td></tr><tr><td>1357</td><td>After You
</td></tr><tr><td>1358</td><td>When Love Comes Your Way
</td></tr><tr><td>1359</td><td>Where, Oh Where
</td></tr></tbody></table>
<h3><a name="1214">1214 &nbsp; Songs By Bobby Short</a></h3>
Bobby Short (piano, vocals) Rollie Bundock (bass) Larry Bunker (drums)
<div class="date">NYC, March 7, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1443</td><td>I Like The Likes Of You
</td></tr><tr><td>1444</td><td>Manhattan
</td></tr><tr><td>1445</td><td>You Make Me Feel So Young
</td></tr><tr><td>1446</td><td>From This Moment On
</td></tr><tr><td>1447</td><td>You Are Not My First Love
</td></tr><tr><td>1448</td><td>Island In The West Indies
</td></tr><tr><td>1449</td><td>Gimme A Pigfoot
</td></tr><tr><td>1450</td><td>Sweet Bye And Bye
</td></tr><tr><td>1451</td><td>I Can't Get Started
</td></tr><tr><td>1452</td><td>Autumn In New York
</td></tr><tr><td>1453</td><td>Suddenly
</td></tr><tr><td>1454</td><td>Now
</td></tr><tr><td>1455</td><td>Dinah
</td></tr></tbody></table>
<h3><a name="1215">1215 &nbsp; Paul Barbarin And His New Orleans Jazz</a></h3>
John Brunious (trumpet) Bob Thomas (trombone) Willie Humphrey (clarinet) Lester Santiago (piano) Danny Barker (banjo, vocals) Milt Hinton (bass) Paul Barbarin (drums)
<div class="date">NYC, January 7, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1405</td><td>Sing On
</td></tr><tr><td>1406</td><td>Someday Sweetheart
</td></tr><tr><td>1407</td><td>Bourbon Street Parade
</td></tr><tr><td>1408</td><td>Just A Little While To Stay Here
</td></tr><tr><td>1409</td><td>Eh La Bas
</td></tr><tr><td>1410</td><td>Bugle Boy March
</td></tr><tr><td>1411</td><td>Crescent Blues
</td></tr><tr><td>1414</td><td>Walking Through The Streets Of The City
</td></tr><tr><td>1415</td><td>I Wish I Could Shimmy Like My Sister Kate
</td></tr></tbody></table>
** also issued on Atlantic SD 1215.
<h3><a name="1216">1216 &nbsp; Dave Pell - Jazz And Romantic Places</a></h3>
Don Fagerquist (trumpet) Ray Sims (trombone) Dave Pell (tenor saxophone) Bob Gordon (baritone saxophone, bass clarinet) Donn Trenner (piano, cello) Tony Rizzi (guitar) Buddy Clark (bass) Bill Richmond (drums)
<div class="date">Hollywood, CA, April 21, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1625</td><td>How Are Things In Glocca Morra
</td></tr><tr><td>1626</td><td>Memphis In June
</td></tr><tr><td>1627</td><td>Deep In The Heart Of Texas
</td></tr><tr><td>1628</td><td>New Orleans
</td></tr></tbody></table>
same personnel
<div class="date">Hollywood, CA, April 23, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1629</td><td>The Island Of Capri
</td></tr><tr><td>1630</td><td>The White Cliffs Of Dover
</td></tr><tr><td>1631</td><td>Sunday In Savannah
</td></tr><tr><td>1632</td><td>Shuffle Off To Buffalo
</td></tr></tbody></table>
same personnel
<div class="date">Los Angeles, CA, April 26, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1633</td><td>Flying Down To Rio
</td></tr><tr><td>1634</td><td>On A Slow Boat To China
</td></tr><tr><td>1635</td><td>London In July
</td></tr><tr><td>1636</td><td>Paris In The Spring
</td></tr></tbody></table>
<h3><a name="1217">1217 &nbsp; Lee Konitz With Warne Marsh</a></h3>
Lee Konitz (alto saxophone) Warne Marsh (tenor saxophone) Sal Mosca (piano -1/4,7) Billy Bauer (guitar) Oscar Pettiford (bass) Kenny Clarke (drums)
<div class="date">NYC, June 14, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1. 1573</td><td>Two Not One
</td></tr><tr><td>2. 1574</td><td>There Will Never Be Another You
</td></tr><tr><td>3. 1575</td><td>Donna Lee
</td></tr><tr><td>4. 1576</td><td>Don't Squawk
</td></tr><tr><td>5. 1577</td><td>Topsy
</td></tr><tr><td>6. 1578</td><td>I Can't Get Started
</td></tr><tr><td>7. 1579</td><td>All Of Me (Background Music)
</td></tr></tbody></table>
Lee Konitz (alto saxophone) Warne Marsh (tenor saxophone) Ronnie Ball (piano) Billy Bauer (guitar) Oscar Pettiford (bass) Kenny Clarke (drums)
<div class="date">NYC, June 15, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1582</td><td>Ronnie's Line
</td></tr></tbody></table>
<h3><a name="1218">1218 &nbsp; Ted Straeter's New York</a></h3>
Bart Wallace (trumpet) Romeo Penque (flute, clarinet, saxophones) Laura Newell (harp) Ted Straeter (piano, vocals) Mundell Lowe or Don Arnone (guitar) Trigger Alpert or Rufus Smith (bass) Ed Shaughnessy or Martin Grupp (drums)
<div class="date">NYC, May 30, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1551</td><td>From This Moment On
</td></tr><tr><td>1552</td><td>All Is Fun
</td></tr><tr><td>1553</td><td>Money Ain't Everything
</td></tr><tr><td>1554</td><td>Ours
</td></tr></tbody></table>
same personnel
<div class="date">NYC, June 5, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1559</td><td>All Of You
</td></tr><tr><td>1560</td><td>You Came A Long Way From St. Louis
</td></tr><tr><td>1561</td><td>What's New
</td></tr><tr><td>1562</td><td>I Guess I'll Have To Change My Plans
</td></tr></tbody></table>
same personnel
<div class="date">NYC, June 6, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1563</td><td>This Is It
</td></tr><tr><td>1564</td><td>It's A Big Wonderful World
</td></tr><tr><td>1565</td><td>Autumn In New York
</td></tr><tr><td>1566</td><td>You're The Top
</td></tr><tr><td>1567</td><td>Something's Gotta Give
</td></tr><tr><td>1568</td><td>Love Me Tomorrow
</td></tr></tbody></table>
<h3><a name="1219">1219 &nbsp; Wilbur DeParis</a></h3>
Doc Cheatham (trumpet -1,2,4) Sidney DeParis (trumpet, tuba) Wilbur DeParis (trombone) Omer Simeon (clarinet) Sonny White (piano) Lee Blair (banjo) Wendell Marshall (bass) Pops Foster (drums)
<div class="date">NYC, April 2, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1. 1476</td><td>Mardi Gras Rag
</td></tr><tr><td>2. 1477</td><td>Milenberg Joys
</td></tr><tr><td>3. 1478</td><td>Flow Gently Sweet Afton
</td></tr><tr><td>4. 1479</td><td>Hot Lips
</td></tr></tbody></table>
Sidney DeParis (trumpet, tuba) Wilbur DeParis (trombone) Omer Simeon (clarinet) Sonny White (piano) Lee Blair (banjo) Wendell Marshall (bass) Pops Foster (drums)
<div class="date">NYC, April 8, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1484</td><td>Are You From Dixie
</td></tr><tr><td>1485</td><td>Yama Yama Man
</td></tr><tr><td>1487</td><td>Madagascar
</td></tr><tr><td>1488</td><td>March Of The Charcoal Grays
</td></tr></tbody></table>
** also issued on Atlantic SD 1219.
<h3><a name="1220">1220 &nbsp; Tony Fruscella</a></h3>
Tony Fruscella (trumpet) Chauncey Welsch (trombone) Allen Eager (tenor saxophone) Danny Bank (baritone saxophone) Bill Triglia (piano) Bill Anthony (bass) Junior Bradley (drums)
<div class="date">NYC, March 29, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1466</td><td>Muy
</td></tr><tr><td>1467</td><td>Salt
</td></tr></tbody></table>
same personnel
<div class="date">NYC, April 1, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1469</td><td>Metropolitan Blues
</td></tr><tr><td>1470</td><td>Raintree County
</td></tr><tr><td>1471</td><td>Blue Serenade
</td></tr><tr><td>1472</td><td>Old Hat
</td></tr><tr><td>1473</td><td>His Master's Voice
</td></tr><tr><td>1474</td><td>I'll Be Seeing You
</td></tr><tr><td>1475</td><td>Let's Play The Blues
</td></tr></tbody></table>
<h3><a name="1221">1221 &nbsp; George Wein - Wein, Women And Song</a></h3>
Ruby Braff (trumpet) Sam Margolis (tenor saxophone) George Wein (piano, vocals) Stan Wheeler (bass) Marquis Foster (drums)
<div class="date">NYC, April 11, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1491</td><td>I'm Gonna Sit Right Down And Write Myself A Letter
</td></tr><tr><td>1492</td><td>All Too Soon
</td></tr><tr><td>1493</td><td>You're Lucky To Me
</td></tr><tr><td>1494</td><td>Back In Your Own Backyard
</td></tr><tr><td>1495</td><td>Once In A While
</td></tr><tr><td>1496</td><td>You Ought To Be In Pictures
</td></tr><tr><td>1497</td><td>Please
</td></tr><tr><td>1498</td><td>Did I Remember
</td></tr><tr><td>1499</td><td>Who Cares (So Long As You Care For Me)
</td></tr></tbody></table>
Bobby Hackett as Wally Wales (trumpet) George Wein (piano, vocals) Bill Pemberton (bass) Jo Jones (drums)
<div class="date">NYC, June 23, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1599</td><td>I Married An Angel
</td></tr><tr><td>1600</td><td>I'm Through With Love
</td></tr><tr><td>1601</td><td>Pennies From Heaven
</td></tr><tr><td>1602</td><td>Why Try To Change Me Now
</td></tr></tbody></table>
<h3><a name="1222">1222 &nbsp; Alec Templeton - The Magic Piano</a></h3>
Alec Templeton (piano) Ben Mortell (guitar) Frank Carroll (bass) Don Lamond (drums)
<div class="date">NYC, April 6, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1252</td><td>Dark Eyes
</td></tr><tr><td>1253</td><td>Bolero
</td></tr></tbody></table>
same personnel
<div class="date">NYC, April 9, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1254</td><td>Tiger Rag
</td></tr><tr><td>1255</td><td>Ida
</td></tr><tr><td>1256</td><td>China Boy
</td></tr><tr><td>1257</td><td>Big Ben Bounce
</td></tr></tbody></table>
same personnel
<div class="date">NYC, April 20, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1265</td><td>Apres Midi D'un Faune
</td></tr><tr><td>1266</td><td>Vocalise
</td></tr><tr><td>1267</td><td>Waltz Antique
</td></tr><tr><td>1268</td><td>Ridin' Thru The Rye
</td></tr></tbody></table>
<h3><a name="1223">1223 &nbsp; Jack Montrose With Bob Gordon</a></h3>
Jack Montrose (tenor saxophone) Bob Gordon (baritone saxophone) Paul Moer (piano) Red Mitchell (bass) Shelly Manne (drums)
<div class="date">Hollywood, CA, May 11, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1637</td><td>A Little Duet
</td></tr><tr><td>1638</td><td>Paradox
</td></tr><tr><td>1639</td><td>When You Wish Upon A Star
</td></tr><tr><td>1640</td><td>Have You Met Miss Jones
</td></tr><tr><td>1641</td><td>Dot's Groovy
</td></tr></tbody></table>
same personnel
<div class="date">Los Angeles, CA, May 12, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1643</td><td>I'm Gonna Move To The Outskirts Of Town
</td></tr><tr><td>1644</td><td>Cecilia
</td></tr><tr><td>1645</td><td>April's Fool
</td></tr><tr><td>1646</td><td>The News And The Weather
</td></tr></tbody></table>
<h3><a name="1224">1224 &nbsp; Lennie Tristano</a></h3>
Lennie Tristano (piano) Peter Ind (bass -1,4) Jeff Morton (drums -1,4)
<div class="date">Lennie Tristano's home studio, NYC, 1954-1955</div>
<table width="100%">
<tbody><tr><td width="15%">1. 4356</td><td>Line Up
</td></tr><tr><td>2. 4357</td><td>Requiem
</td></tr><tr><td>3. 4358</td><td>Turkish Mambo
</td></tr><tr><td>4. 4359</td><td>East Thirty-Second Street
</td></tr></tbody></table>
Lee Konitz (alto saxophone) Lennie Tristano (piano) Gene Ramey (bass) Art Taylor (drums)
<div class="date">"The Sing-Song Room, Confucius Restaurant", NYC, 1st set, June 11, 1955</div>
<table width="100%">
<tbody><tr><td width="15%"></td><td>If I Had You
</td></tr></tbody></table>
same personnel
<div class="date">"The Sing-Song Room, Confucius Restaurant", NYC, 2nd set, June 11, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">4364</td><td>These Foolish Things
</td></tr><tr><td>4366</td><td>You Go To My Head
</td></tr><tr><td>4367</td><td>All The Things You Are
</td></tr></tbody></table>
same personnel
<div class="date">"The Sing-Song Room, Confucius Restaurant", NYC, 4th set, June 11, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">4368</td><td>A Ghost Of A Chance
</td></tr></tbody></table>
** part of Mosaic MQ10-174, MD6-174.
<h3><a name="1225">1225 &nbsp; Jess Stacy And The Famous Sidemen - Tribute To Benny Goodman</a></h3>
Ziggy Elman (trumpet) Murray McEachern (trombone) Heinie Beau (alto saxophone, clarinet, arranger) Vido Musso (tenor saxophone) Chuck Gentry (baritone saxophone) Jess Stacy (piano) Allan Reuss (guitar) Artie Shapiro (bass) Nick Fatool (drums)
<div class="date">Hollywood, CA, April 15, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1277</td><td>Roll 'Em
</td></tr><tr><td>1278</td><td>Where Or When
</td></tr><tr><td>1279</td><td>Sing, Sing, Sing
</td></tr><tr><td>1280</td><td>Let's Dance
</td></tr><tr><td>1281</td><td>Goodbye
</td></tr><tr><td>1282</td><td>King Porter Stomp
</td></tr></tbody></table>
Ziggy Elman (trumpet) Ted Vesely (trombone) Heinie Beau (alto saxophone, arranger) Babe Russin (tenor saxophone) Joe Koch (baritone saxophone) Jess Stacy (piano) Al Hendrickson (guitar) Artie Shapiro (bass) Nick Fatool (drums)
<div class="date">Hollywood, CA, April 29, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1283</td><td>Don't Be That Way
</td></tr><tr><td>1284</td><td>Sometimes I'm Happy
</td></tr><tr><td>1285</td><td>When Buddha Smiles
</td></tr><tr><td>1286</td><td>Down South Camp Meetin'
</td></tr></tbody></table>
Jess Stacy (piano) Artie Shapiro (bass) Nick Fatool (drums)
<div class="date">Hollywood, CA, October 6, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1693</td><td>You Turned The Tables On Me
</td></tr><tr><td>1694</td><td>I Must Have That Man
</td></tr><tr><td>1695</td><td>Gee Baby, Ain't I Good To You
</td></tr><tr><td>1696</td><td>Blues For Otis Ferguson
</td></tr></tbody></table>
<h3><a name="1226">1226 &nbsp; Betty Bennett - Nobody Else But Me</a></h3>
John Cave (French horn) Arthur Gleghorn, Harry Klee (flute) Philip Memoli (oboe) Gus Bivona (clarinet) Dave Pell (bass clarinet) Katherine Johnk (harp) Andre Previn (piano) Ralph Pena (bass) Shelly Manne (drums) Betty Bennett (vocals)
<div class="date">Los Angeles, CA, October 4, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1701</td><td>This Is The Moment
</td></tr><tr><td>1702</td><td>Nobody Else But Me
</td></tr><tr><td>1703</td><td>Have Yourself A Merry Little Christmas
</td></tr><tr><td>1704</td><td>The Next Time I Care
</td></tr></tbody></table>
Shorty Rogers (trumpet, flugelhorn) Frank Rosolino (trombone) Harry Klee (alto saxophone) Bob Cooper (tenor saxophone) Jimmy Giuffre (baritone saxophone) Andre Previn (piano) Barney Kessel (guitar) Ralph Pena (bass) Shelly Manne (drums) Betty Bennett (vocals)
<div class="date">Los Angeles, CA, October 6, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1705</td><td>You Took Advantage Of Me
</td></tr><tr><td>1706</td><td>My Man's Gone Now
</td></tr><tr><td>1707</td><td>You're Driving Me Crazy
</td></tr><tr><td>1708</td><td>Mountain Greenery
</td></tr></tbody></table>
Irv Cottler (drums) replaces Manne
<div class="date">Los Angeles, CA, October 7, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1709</td><td>Treat Me Rough
</td></tr><tr><td>1710</td><td>Island In The West Indies
</td></tr><tr><td>1711</td><td>Sidewalks Of Cuba
</td></tr><tr><td>1712</td><td>Tomorrow Mountain
</td></tr></tbody></table>
<h3><a name="1227">1227 &nbsp; Erroll Garner - The Greatest Garner</a></h3>
Erroll Garner (piano) Leonard Gaskin (bass) Charlie Smith (drums)
<div class="date">NYC, July 20, 1949</div>
<table width="100%">
<tbody><tr><td width="15%">240</td><td>Reverie
</td></tr><tr><td>241</td><td>Turquoise
</td></tr><tr><td>242</td><td>Blue And Sentimental
</td></tr><tr><td>243</td><td>Pavanne Mood (The Lamp Is Low)
</td></tr><tr><td>244</td><td>Flamingo
</td></tr><tr><td>245</td><td>Skylark
</td></tr><tr><td>246</td><td>I Can't Give You Anything But Love
</td></tr><tr><td>247</td><td>Impressions (Clair De Lune Improvisation)
</td></tr><tr><td>249</td><td>The Way You Look Tonight
</td></tr></tbody></table>
Erroll Garner (piano) John Simmons (bass) Doc West (drums)
<div class="date">NYC, May 12, 1950</div>
<table width="100%">
<tbody><tr><td width="15%">422</td><td>Summertime
</td></tr><tr><td>429</td><td>I'm Confessin'
</td></tr><tr><td>432</td><td>I May Be Wrong (But I Think You're Wonderful)
</td></tr></tbody></table>
<h3><a name="1228">1228 &nbsp; Chris Connor</a></h3>
Chris Connor (vocals) unidentified orchestra, Ralph Burns (conductor)
<div class="date">NYC, January 19, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1835</td><td>My April Heart
</td></tr><tr><td>1836</td><td>When The Wind Was Green
</td></tr><tr><td>1837</td><td>He Was Too Good To Me
</td></tr><tr><td>1838</td><td>Something To Live For
</td></tr></tbody></table>
John Lewis (piano) Barry Galbraith (guitar) Oscar Pettiford (bass) Connie Kay (drums) Chris Connor (vocals)
<div class="date">NYC, January 23, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1853</td><td>Where Are You
</td></tr><tr><td>1854</td><td>I Get A Kick Out Of You
</td></tr><tr><td>1855</td><td>Ev'ry Time
</td></tr><tr><td>1856</td><td>Almost Like Being In Love
</td></tr></tbody></table>
Nick Travis (trumpet) Ray Beckenstein, Sam Markowitz (alto saxophone) Zoot Sims, Al Young (tenor saxophone) Danny Bank (baritone saxophone) Moe Wechsler (piano) Barry Galbraith (guitar) Milt Hinton (bass) Osie Johnson (drums) Chris Connor (vocals)
<div class="date">NYC, February 8, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1874</td><td>You Make Me Feel So Young
</td></tr><tr><td>1875</td><td>Anything Goes
</td></tr><tr><td>1876</td><td>Way Out There
</td></tr><tr><td>1877</td><td>Get Out Of Town
</td></tr></tbody></table>
** also issued on Atlantic SD 1228.
<h3><a name="1229">1229 &nbsp; The Teddy Charles Tentet</a></h3>
Art Farmer as Peter Urban (trumpet) Don Butterfield (tuba) Gigi Gryce (alto saxophone) J.R. Monterose (tenor saxophone) George Barrow (baritone saxophone) Teddy Charles (vibraphone, arranger) Mal Waldron (piano) Jimmy Raney (guitar) Teddy Kotick (bass) Joe Harris (drums) Jimmy Giuffre (arranger)
<div class="date">Coastal Recording Studios, NYC, January 6, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1807</td><td>Nature Boy
</td></tr><tr><td>1808</td><td>The Quiet Time
</td></tr></tbody></table>
Art Farmer as Peter Urban (trumpet) Don Butterfield (tuba) Gigi Gryce (alto saxophone) J.R. Monterose (tenor saxophone) George Barrow (baritone saxophone) Teddy Charles (vibraphone, arranger) Mal Waldron (piano) Jimmy Raney (guitar) Teddy Kotick (bass) Joe Harris (drums) Bob Brookmeyer, Gil Evans (arranger)
<div class="date">Coastal Recording Studios, NYC, January 11, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1813</td><td>Green Blues
</td></tr><tr><td>1814</td><td>You Go To My Head
</td></tr></tbody></table>
Art Farmer as Peter Urban (trumpet) Don Butterfield (tuba) Gigi Gryce (alto saxophone) J.R. Monterose (tenor saxophone) Sol Schlinger (baritone saxophone) Teddy Charles (vibraphone, arranger) Mal Waldron (piano, arranger) Jimmy Raney (guitar) Teddy Kotick (bass) Joe Harris (drums) George Russell (arranger)
<div class="date">Coastal Recording Studios, NYC, January 17, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1831</td><td>Vibrations
</td></tr><tr><td>1832</td><td>The Emperor
</td></tr><tr><td>1833</td><td>Lydian M-1
</td></tr></tbody></table>
<h3><a name="1230">1230 &nbsp; Bobby Short</a></h3>
Pete Candoli (trumpet) Bobby Short (piano, vocals) Buddy Woodson (bass) Maurice Russell (drums)
<div class="date">Los Angeles, CA, November 15, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1791</td><td>Down With Love
</td></tr><tr><td>1792</td><td>I've Got The World On A String
</td></tr><tr><td>1793</td><td>I've Got Five Dollars
</td></tr><tr><td>1794</td><td>Sand In My Shoes
</td></tr><tr><td>1795</td><td>Any Place I Hang My Hat Is Home
</td></tr></tbody></table>
same personnel
<div class="date">Los Angeles, CA, November 16, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1796</td><td>Bye Bye Blackbird
</td></tr><tr><td>1797</td><td>Carioca
</td></tr><tr><td>1801</td><td>The Most Beautiful Girl In The World
</td></tr><tr><td>1802</td><td>Hottentot Potentate
</td></tr><tr><td>1803</td><td>Fun To Be Fooled
</td></tr><tr><td>1804</td><td>Bedelia
</td></tr><tr><td>1805</td><td>At The Moving Picture Ball
</td></tr></tbody></table>
<h3><a name="1231">1231 &nbsp; The Modern Jazz Quartet - Fontessa</a></h3>
Milt Jackson (vibraphone) John Lewis (piano) Percy Heath (bass) Connie Kay (drums)
<div class="date">NYC, January 22, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1843</td><td>Woody'n You
</td></tr><tr><td>1844</td><td>Willow Weep For Me
</td></tr><tr><td>1845</td><td>Fontessa
</td></tr><tr><td>1846</td><td>Versailles (Porte De Versailles)
</td></tr><tr><td>1847</td><td>Angel Eyes
</td></tr><tr><td>1848</td><td>Over The Rainbow
</td></tr></tbody></table>
same personnel
<div class="date">Rudy Van Gelder Studio, Hackensack, NJ, February 14, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2630</td><td>Bluesology
</td></tr></tbody></table>
<h3><a name="1232">1232 &nbsp; Shorty Rogers - Martians, Come Back!</a></h3>
Shorty Rogers (trumpet, flugelhorn) Jimmy Giuffre (clarinet, tenor, baritone saxophone) Lou Levy (piano) Ralph Pena (bass) Shelly Manne (drums)
<div class="date">Los Angeles, CA, October 26, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1742</td><td>Planetarium
</td></tr><tr><td>1743</td><td>Martians, Come Back!
</td></tr></tbody></table>
same personnel
<div class="date">Los Angeles, CA, November 3, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1745</td><td>Papouche
</td></tr><tr><td>1748</td><td>Lotus Bud
</td></tr></tbody></table>
Conte Candoli, Pete Candoli, Harry Edison, Don Fagerquist (trumpet) Shorty Rogers (trumpet, flugelhorn) Lou Levy (piano) Ralph Pena (bass) Shelly Manne (drums)
<div class="date">Los Angeles, CA, December 6, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1771</td><td>Serenade In Sweets
</td></tr><tr><td>1772</td><td>Astral Alley
</td></tr></tbody></table>
Shorty Rogers (trumpet, flugelhorn) Bob Enevoldsen (valve trombone) John Graas (French horn) Paul Sarmento (tuba) Jimmy Giuffre (clarinet, tenor, baritone saxophone) Bud Shank (alto saxophone) Lou Levy (piano) Ralph Pena (bass) Shelly Manne (drums)
<div class="date">Los Angeles, CA, December 9, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1776</td><td>Baklava Bridge
</td></tr><tr><td>1777</td><td>Chant Of The Cosmos
</td></tr></tbody></table>
Harry Edison (trumpet) Shorty Rogers (trumpet, flugelhorn) Bud Shank (alto saxophone) Pete Jolly (piano) Barney Kessel (guitar) Leroy Vinnegar (bass) Shelly Manne (drums)
<div class="date">Los Angeles, CA, December 16, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1787</td><td>Dickie's Dream
</td></tr><tr><td>1788</td><td>Moten Swing
</td></tr></tbody></table>
** also issued on Atlantic SD 1232.
<h3><a name="1233">1233 &nbsp; Wilbur DeParis - Marchin' And Shoutin'</a></h3>
Sidney DeParis (trumpet, vocals) Wilbur DeParis (trombone) Omer Simeon (clarinet) Don Kirkpatrick (piano) Eddie Gibbs (banjo) Harold Jackson (bass) Freddie Moore (drums)
<div class="date">NYC, September 11, 1952</div>
<table width="100%">
<tbody><tr><td width="15%">879</td><td>Hindustan
</td></tr><tr><td>880</td><td>Shreveport Stomp
</td></tr><tr><td>881</td><td>The Pearls
</td></tr><tr><td>882</td><td>Tres Moutarde
</td></tr><tr><td>883</td><td>When The Saints Go Marching In
</td></tr><tr><td>884</td><td>The Martinique
</td></tr><tr><td>885</td><td>Under The Double Eagle
</td></tr><tr><td>886</td><td>Battle Hymn Of The Republic
</td></tr><tr><td>887</td><td>Prelude In C Sharp Minor
</td></tr><tr><td>888</td><td>Marchin' And Swingin'
</td></tr></tbody></table>
** also issued on Atlantic SD 1233.
<h3><a name="1234">1234 &nbsp; Joe Turner - The Boss Of The Blues</a></h3>
Joe Newman (trumpet) Lawrence Brown (trombone) Pete Brown (alto saxophone) Frank Wess (tenor saxophone) Pete Johnson (piano) Freddie Green (guitar) Walter Page (bass) Cliff Leeman (drums) Joe Turner (vocals)
<div class="date">NYC, March 6, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1915</td><td>Low Down Dog
</td></tr><tr><td>1916</td><td>Roll 'Em Pete
</td></tr><tr><td>1917</td><td>Cherry Red
</td></tr><tr><td>1918</td><td>How Long Blues
</td></tr><tr><td>1919</td><td>Piney Brown Blues
</td></tr><tr><td>1920</td><td>Morning Glories
</td></tr></tbody></table>
Jimmy Nottingham (trumpet) Seldon Powell (tenor saxophone) replaces Newman, Wess
<div class="date">NYC, March 7, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1921</td><td>I Want A Little Girl
</td></tr><tr><td>1922</td><td>St. Louis Blues
</td></tr><tr><td>1923</td><td>You're Driving Me Crazy
</td></tr><tr><td>1924</td><td>Pennies From Heaven
</td></tr><tr><td>1925</td><td>Wee Baby Blues
</td></tr></tbody></table>
** also issued on Atlantic SD 1234, SD 8812.
<h3><a name="1235">1235 &nbsp; Phineas Newborn Jr. - Here Is Phineas</a></h3>
Phineas Newborn Jr. (piano) Calvin Newborn (guitar) Oscar Pettiford (bass) Kenny Clarke (drums)
<div class="date">NYC, May 3, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1977</td><td>Daahoud
</td></tr><tr><td>1978</td><td>All The Things You Are
</td></tr><tr><td>1980</td><td>Barbados
</td></tr><tr><td>1981</td><td>Afternoon In Paris
</td></tr></tbody></table>
Phineas Newborn Jr. (piano) Oscar Pettiford (bass -1,2) Kenny Clarke (drums -1,2)
<div class="date">NYC, May 4, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1. 1982</td><td>Celia
</td></tr><tr><td>2. 1985</td><td>I'm Beginning To See The Light
</td></tr><tr><td>3. 1986</td><td>The More I See You
</td></tr><tr><td>4. 1987</td><td>Newport Blues
</td></tr></tbody></table>
** also issued on Atlantic SD 1235.
<h3><a name="1236">1236 &nbsp; Cy Walter Plays Richard Rodgers Compositions - Rodgers Revisited</a></h3>
Cy Walter (piano)
<div class="date">NYC, April 15, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1951</td><td>March Of The Siamese Children
</td></tr><tr><td>1952</td><td>Soliloquy
</td></tr><tr><td>1953</td><td>Slaughter On 10th Avenue
</td></tr><tr><td>1954</td><td>Getting To Know You
</td></tr><tr><td>1955</td><td>Carousel Waltzes
</td></tr><tr><td>1956</td><td>I Have Dreamed
</td></tr><tr><td>1957</td><td>Wait Till You See Her
</td></tr><tr><td>1958</td><td>Lover
</td></tr><tr><td>1959</td><td>The Gentleman Is A Dope
</td></tr><tr><td>1960</td><td>Hello Young Lovers
</td></tr><tr><td>1961</td><td>Sing For Your Supper
</td></tr><tr><td>1963</td><td>This Can't Be Love
</td></tr><tr><td>1964</td><td>Suzie Is A Good Thing
</td></tr></tbody></table>
<h3><a name="1237">1237 &nbsp; Charles Mingus - Pithecanthropus Erectus</a></h3>
Jackie McLean (alto saxophone) J.R. Monterose (tenor saxophone -1/3) Mal Waldron (piano) Charles Mingus (bass) Willie Jones (drums)
<div class="date">Audio-Video Studios, NYC, January 30, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1. 1865</td><td>Pithecanthropus Erectus: Evolution / Superiority-Complex / Decline / Destruction
</td></tr><tr><td>2. 1866</td><td>A Foggy Day
</td></tr><tr><td>3. 1868</td><td>Love Chant
</td></tr><tr><td>4. 1869</td><td>Profile Of Jackie
</td></tr></tbody></table>
** also issued on Atlantic SD 8809.<br>
** part of Rhino R2 72871.
<h3><a name="1238">1238 &nbsp; The Jimmy Giuffre Clarinet</a></h3>
Harry Edison, Shorty Rogers, Jack Sheldon (trumpet) Jimmy Giuffre (clarinet) Bob Cooper (tenor saxophone, oboe) Dave Pell (tenor saxophone, English horn) Marty Berman (baritone saxophone, bassoon) Ralph Pena (bass) Stan Levey (drums)
<div class="date">Capitol Studios, Los Angeles, CA, March 21, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1993</td><td>Down Home
</td></tr><tr><td>1994</td><td>My Funny Valentine
</td></tr><tr><td>1995</td><td>Quiet Cook
</td></tr><tr><td>1996</td><td>So Low
</td></tr></tbody></table>
Bud Shank (alto flute) Buddy Collette (alto clarinet, flute) Jimmy Giuffre (clarinet) Harry Klee (bass clarinet, bass flute) Jimmy Rowles (piano, celeste) Shelly Manne (drums)
<div class="date">Capitol Studios, Los Angeles, CA, March 22, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1989</td><td>The Sheepherder
</td></tr><tr><td>1990</td><td>The Sidepipers
</td></tr><tr><td>1991</td><td>Fascinating Rhythm
</td></tr><tr><td>1992</td><td>Deep Purple
</td></tr></tbody></table>
** part of Mosaic MQ10-176, MD6-176.
<h3><a name="1239">1239 &nbsp; Various Artists - Rock And Roll Forever</a></h3>
Willis Jackson (tenor saxophone) Harry Van Walls (piano) Connie Kay (drums) The Clovers (doo wop group) and others
<div class="date">NYC, December 19, 1951</div>
<table width="100%">
<tbody><tr><td width="15%">755</td><td>One Mint Julep
</td></tr></tbody></table>
unknown (trumpet) Willis Jackson (tenor saxophone) 2 unknown (saxophones) Harry Van Walls (piano) unknown (guitar) unknown (bass) Connie Kay (drums) Ruth Brown (vocals)
<div class="date">NYC, February 13, 1952</div>
<table width="100%">
<tbody><tr><td width="15%">804</td><td>5-10-15 Hours
</td></tr></tbody></table>
Taft Jordan (trumpet) unknown (saxophones) unknown (piano) Mickey Baker (guitar) unknown (bass) Connie Kay (drums) Ruth Brown (vocals)
<div class="date">NYC, December 19, 1952</div>
<table width="100%">
<tbody><tr><td width="15%">960</td><td>Mama, He Treats Your Daughter Mean
</td></tr></tbody></table>
Sam Taylor (tenor saxophone) Harry Van Walls (piano) possibly Bill Harris (guitar) unknown (bass) Connie Kay (drums) Charlie White (lead vocals) Matthew McQuater (tenor vocals) Harold Lucas (baritone vocals) Harold Winley (bass vocals)
<div class="date">NYC, March 4, 1953</div>
<table width="100%">
<tbody><tr><td width="15%">1017</td><td>Good Lovin'
</td></tr></tbody></table>
Jesse Drakes (trumpet) Sam Taylor (tenor saxophone) Dave McRae (baritone saxophone) Ray Charles (piano, vocals) Mickey Baker (guitar) Lloyd Trotman (bass) Connie Kay (drums)
<div class="date">NYC, May 17, 1953</div>
<table width="100%">
<tbody><tr><td width="15%">1065</td><td>It Should Have Been Me
</td></tr></tbody></table>
Sam Taylor (tenor saxophone) Jesse Stone (piano) Walter Adams, Mickey Baker (guitar) unknown (bass, drums) Clyde McPhatter (lead tenor vocals) Andrew Thrasher (tenor vocals) Gerhart Thrasher (baritone vocals) Willie Ferbee (bass vocals)
<div class="date">NYC, August 9, 1953</div>
<table width="100%">
<tbody><tr><td width="15%">1105</td><td>Money Honey
</td></tr></tbody></table>
unknown (tenor saxophone, vibraphone, piano, bass, drums) Jimmy Oliver (guitar) Clyde McPhatter (lead tenor vocals) Gerhart Thrasher (tenor vocals) Andrew Thrasher (baritone vocals) Bill Pinkney (bass vocals)
<div class="date">NYC, February 4, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1203</td><td>Honey Love
</td></tr></tbody></table>
unknown (trumpet) Wilbur DeParis (trombone) Sam Taylor (tenor saxophone) Haywood Henry (baritone saxophone) Jesse Stone (piano) Mickey Baker (guitar) Lloyd Trotman (bass) Connie Kay (drums) Joe Turner (vocals) unknown (vocal group)
<div class="date">NYC, February 15, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1209</td><td>Shake, Rattle And Roll
</td></tr></tbody></table>
Sam Taylor (tenor saxophone) unknown (baritone saxophone) unknown (piano) unknown (guitar) unknown (bass) Connie Kay (drums) LaVern Baker (vocals) The Gliders (vocal group)
<div class="date">NYC, October 20, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1334</td><td>Tweedlee Dee
</td></tr></tbody></table>
Joe Bridgewater, Charles Whitley (trumpet) Don Wilkerson (tenor saxophone) David Newman (baritone saxophone) Ray Charles (piano, vocals) Wesley Jackson (guitar) Jimmy Bell (bass) Glenn Brooks (drums)
<div class="date">Atlanta, GA, November 18, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1383</td><td>I've Got A Woman
</td></tr></tbody></table>
unknown (trumpet) unknown (alto saxophone) Al Sears (tenor saxophone) unknown (baritone saxophone) Jesse Stone (piano, director) unknown (guitar) unknown (bass) probably Connie Kay (drums) Joe Turner (vocals)
<div class="date">NYC, January 28, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1426</td><td>Hide And Seek
</td></tr><tr><td>1427</td><td>Flip, Flop And Fly
</td></tr></tbody></table>
Sam Taylor (tenor saxophone) unknown (baritone saxophone) unknown (piano) Mickey Baker (guitar) unknown (bass) Connie Kay (drums) LaVern Baker (vocals) unknown (vocal group)
<div class="date">NYC, February 20, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1433</td><td>Bop-Ting-A-Ling
</td></tr></tbody></table>
Andrew "Goon" Gardner (alto saxophone) Eddie Chamblee (tenor saxophone) McKinley Easton (baritone saxophone) John Young (piano) T-Bone Walker (guitar, vocals) Ransom Knowling (bass) Leroy Jackson (drums)
<div class="date">Chicago, IL, April 21, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1520</td><td>T-Bone Shuffle
</td></tr></tbody></table>
** also issued on Atlantic LP 8010.
<h3><a name="1240">1240 &nbsp; Chris Connor - He Loves Me, He Loves Me Not</a></h3>
Chris Connor (vocals) unidentified orchestra, Ralph Burns (arranger, conductor)
<div class="date">NYC, June 5, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2006</td><td>'Round Midnight
</td></tr><tr><td>2007</td><td>But Not For Me
</td></tr><tr><td>2008</td><td>Oh! You Crazy Moon
</td></tr><tr><td>2009</td><td>High On A Windy Hill
</td></tr></tbody></table>
same personnel
<div class="date">NYC, June 6, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2010</td><td>Why Can't I
</td></tr><tr><td>2011</td><td>Suddenly It's Spring
</td></tr><tr><td>2012</td><td>Angel Eyes
</td></tr><tr><td>2013</td><td>You Stepped Out Of A Dream
</td></tr></tbody></table>
same personnel
<div class="date">NYC, August 7, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2073</td><td>I Guess I'll Hang My Tears Out To Dry
</td></tr><tr><td>2074</td><td>Thursday's Child
</td></tr><tr><td>2075</td><td>I Wonder What Became Of Me
</td></tr><tr><td>2076</td><td>About The Blues
</td></tr></tbody></table>
<h3><a name="1241">1241 &nbsp; Bill Russo - The World Of Alcina</a></h3>
Bill Porter, Bill Russo (trombone) Sandy Mosse, Bill Trujillo (tenor saxophone) Eddie Baker (piano) Israel Crosby (bass) Dominic "Mickey" Simonetta (drums)
<div class="date">Chicago, IL, April 18, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1621</td><td>Lady (Under The Greenwood Tree)
</td></tr><tr><td>1622</td><td>Canon (The First Saturday In May)
</td></tr><tr><td>1623</td><td>Ab (Speculum)
</td></tr></tbody></table>
omit Porter, Trujillo
<div class="date">Chicago, IL, April 19, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1616</td><td>Bill's Blues
</td></tr><tr><td>1618</td><td>L'Affaire Bugs
</td></tr><tr><td>1620</td><td>Ballad For My Sister
</td></tr></tbody></table>
Don Geraci, John Howell, Dave Mulholland, Al Muller, Porky Panico (trumpet) Mark Dunn, Earl Hoffman, Paul Krum, Bill Porter, Paul Severson, Tommy Shepard (trombone) Bill Russo (trombone, composer, arranger, conductor) Frank Brouk, Phil Farkus (French horn) Don Habner (tuba) Lenny Druss, Bart Grimes, Gus Jean, Don Kolbart, Vito Price, Mike Simpson, Kenny Soderblom, Phil Wing (saxophones, woodwinds) Eddie Baker (piano) Earl Backus (guitar) Mel Schmidt (bass) Dominic "Mickey" Simonetta (drums)
<div class="date">Chicago, IL, May 6, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1997</td><td>The World Of Alcina: Ballet Music
</td></tr><tr><td>-</td><td>The World Of Alcina: 1st Dance: Solo Of Girl
</td></tr><tr><td>-</td><td>The World Of Alcina: 2nd Dance: Solo Of Boy
</td></tr><tr><td>-</td><td>The World Of Alcina: 3rd Dance: Chorus And Solo Of Girl
</td></tr><tr><td>-</td><td>The World Of Alcina: 4th Dance: Duet For Boy And Girl
</td></tr><tr><td>-</td><td>The World Of Alcina: 5th Dance: Chorus-Solo Of Boy/Solo Of Girl Ensemble
</td></tr></tbody></table>
<h3><a name="1242">1242 &nbsp; Milt Jackson - Ballads And Blues</a></h3>
Lucky Thompson (tenor saxophone) Milt Jackson (vibraphone) John Lewis (piano) Skeeter Best (guitar) Oscar Pettiford (bass) Kenny Clarke (drums)
<div class="date">NYC, January 17, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1828</td><td>Hello
</td></tr><tr><td>1829</td><td>Bright Blues
</td></tr><tr><td>1830</td><td>How High The Moon
</td></tr></tbody></table>
Ralph Burns, Milt Jackson (vibraphone) John Lewis (piano) Barry Gailbraith (guitar) Oscar Pettiford (bass) Kenny Clarke (drums)
<div class="date">NYC, January 21, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1839</td><td>So In Love
</td></tr><tr><td>1841</td><td>They Didn't Believe Me
</td></tr><tr><td>1842</td><td>Solitude
</td></tr></tbody></table>
Milt Jackson (vibraphone) Barney Kessel (guitar) Percy Heath (bass) Lawrence Marable (drums)
<div class="date">Rudy Van Gelder Studio, Hackensack, NJ, February 14, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2625</td><td>The Song Is Ended
</td></tr><tr><td>2626</td><td>Gerry's Blues
</td></tr><tr><td>2628</td><td>These Foolish Things
</td></tr></tbody></table>
<h3><a name="1243">1243 &nbsp; Sylvia Syms Sings</a></h3>
Barbara Carroll (piano) Joe Shulman (bass) Herb Wasserman (drums) Sylvia Syms (vocals)
<div class="date">NYC, March 8, 1952</div>
<table width="100%">
<tbody><tr><td width="15%">812</td><td>Love Walked In
</td></tr><tr><td>813</td><td>There's Something About An Old Love
</td></tr><tr><td>814</td><td>Mountain Greenery
</td></tr><tr><td>815</td><td>Down In The Depths On The Ninetieth Floor
</td></tr><tr><td>816</td><td>Can't You Just See Yourself
</td></tr><tr><td>817</td><td>What Is There To Say
</td></tr><tr><td>818</td><td>Lonely Woman
</td></tr><tr><td>819</td><td>Imagination
</td></tr></tbody></table>
Don Elliott (trumpet, mellophone, vibraphone) Kai Winding (trombone) Danny Bank (flute) Al Cohn (tenor saxophone) Elliot Eberhard (piano) Clyde Lombardi (bass) Jimmy Campbell (drums) Sylvia Syms (vocals) Johnny Richards (arranger, conductor)
<div class="date">NYC, February 9, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1205</td><td>Comes Love
</td></tr><tr><td>1206</td><td>Tea For Two
</td></tr><tr><td>1207</td><td>I Want A Little Boy
</td></tr><tr><td>1208</td><td>Paradise
</td></tr></tbody></table>
<h3><a name="1244">1244 &nbsp; Midnight At Mabel Mercer's</a></h3>
George Cory or Sam Hamilton (piano) Milt Hinton (bass) Mabel Mercer (vocals)
<div class="date">NYC, June 17, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2030</td><td>Blame It On My Youth
</td></tr><tr><td>2031</td><td>Poor Pierrot
</td></tr><tr><td>2032</td><td>It's A Lie, It's A Fake!
</td></tr><tr><td>2033</td><td>Young And Foolish
</td></tr><tr><td>2034</td><td>Is It Always Like This
</td></tr><tr><td>2035</td><td>Wait Till You See Her
</td></tr></tbody></table>
same personnel
<div class="date">NYC, June 17 &amp; 18, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2036</td><td>Just Once Around The Clock
</td></tr><tr><td>2037</td><td>Wouldn't It Be Loverly
</td></tr><tr><td>2038</td><td>Lonely Little Boy
</td></tr><tr><td>2039</td><td>Sonnet
</td></tr><tr><td>2040</td><td>Lucky To Be Me
</td></tr><tr><td>2041</td><td>He Was Too Good To Me
</td></tr><tr><td>2042</td><td>Lazy Afternoon
</td></tr><tr><td>2043</td><td>Some Other Time
</td></tr><tr><td>2044</td><td>Walk-Up
</td></tr><tr><td>2045</td><td>Mandy Make Up Your Mind
</td></tr></tbody></table>
<h3><a name="1245">1245 &nbsp; Patty McGovern/Thomas Talbert - Wednesday's Child</a></h3>
Joe Wilder (trumpet) Jim Buffington (French horn) Al Block or Joe Soldo, Jerry Sanfino (flute) Sey Schwartberg (bassoon) Danny Bank, Ernest Bright (clarinet) Barry Galbraith (guitar) Arnold Fishkin, Jack Lesberg (bass) Osie Johnson, Don Lamond (drums) Patty McGovern (vocals) Tom Talbert (arranger, conductor)
<div class="date">NYC, August, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">4437</td><td>Alone Together
</td></tr><tr><td>4438</td><td>I Like Snow
</td></tr><tr><td>4439</td><td>Crazy He Calls Me
</td></tr><tr><td>4440</td><td>You Don't Know What Love Is
</td></tr><tr><td>4441</td><td>All In Fun
</td></tr><tr><td>4442</td><td>Hooray For Love
</td></tr><tr><td>4443</td><td>Lonely Town
</td></tr><tr><td>4444</td><td>Wednesday's Child
</td></tr><tr><td>4445</td><td>Love Isn't Everything
</td></tr><tr><td>4446</td><td>Get Out Of Town
</td></tr><tr><td>4447</td><td>Winter Song
</td></tr><tr><td>4448</td><td>By Myself
</td></tr></tbody></table>
<h3><a name="1246">1246 &nbsp; Lars Gullin - Baritone Sax</a></h3>
Georg Vernon (trombone) Arne Domnerus (alto saxophone, clarinet) Carl-Henrik Norin (tenor saxophone) Rune Falk, Lars Gullin (baritone saxophone) Rune Ofwerman (piano) George Riedel (bass) Bert Dahlander (drums)
<div class="date">Stockholm, Sweden, April 23, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">mr1037</td><td>Fedja
</td></tr><tr><td>mr1040</td><td>Perntz
</td></tr></tbody></table>
Lars Gullin (baritone saxophone) Rune Ofwerman (piano) Bengt Carlsson (bass) Bert Dahlander (drums)
<div class="date">Stockholm, Sweden, April 24, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">mr1041</td><td>All Of Me
</td></tr></tbody></table>
Ake Persson (trombone) Lars Gullin (baritone saxophone) Rune Ofwerman (piano) George Riedel (bass) Bert Dahlander (drums)
<div class="date">Stockholm, Sweden, April 25, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">mr1049</td><td>So What
</td></tr></tbody></table>
Jan Allan, Weine Renliden, Nisse Skoog, Bengt-Arne Wallin (trumpet) Gordon Ohlsson, Ake Persson, Georg Vernon (trombone) Arne Domnerus (alto saxophone) Rolf Blomquist, Carl-Henrik Norin (tenor saxophone) Rune Falk, Lars Gullin (baritone saxophone) Rune Ofwerman (piano) George Riedel (bass) Bert Dahlander (drums) Gosta Theselius (arranger)
<div class="date"></div>
<table width="100%">
<tbody><tr><td width="15%">mr1045</td><td>Summertime
</td></tr><tr><td>mr1048</td><td>A Foggy Day
</td></tr></tbody></table>
Ake Persson (trombone) Arne Domnerus (alto saxophone) Lars Gullin (baritone saxophone) Rune Ofwerman (piano) George Riedel (bass) Bert Dahlander (drums)
<div class="date">Stockholm, Sweden, April 26, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">mr1052</td><td>Mean To Me
</td></tr></tbody></table>
<h3><a name="1247">1247 &nbsp; The Modern Jazz Quartet At Music Inn - Guest Artist: Jimmy Giuffre</a></h3>
Milt Jackson (vibraphone) John Lewis (piano) Percy Heath (bass) Connie Kay (drums) with guest artist: Jimmy Giuffre (clarinet -2,4,5)
<div class="date">"Music Inn", Lenox, MA, August 28, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1. 2096</td><td>Oh Bess, Oh Where's My Bess
</td></tr><tr><td>2. 2097</td><td>A Fugue For Music Inn
</td></tr><tr><td>3. 2098</td><td>Two Degrees East, Three Degrees West
</td></tr><tr><td>4. 2099</td><td>Serenade
</td></tr><tr><td>5. 2100</td><td>Fun
</td></tr><tr><td>6. 2101</td><td>Sun Dance
</td></tr><tr><td>7. 2102</td><td>The Man That Got Away
</td></tr><tr><td>8. 2103</td><td>A Morning In Paris
</td></tr><tr><td>9. 2104</td><td>Variation No. 1 On God Rest Ye Merry, Gentlemen
</td></tr></tbody></table>
<h3><a name="1248">1248 &nbsp; The Clovers</a></h3>
Bill Harris (guitar) John Bailey (lead vocals) Matthew McQuater (tenor vocals) Harold Lucas (baritone vocals) Harold Winley (bass vocals)
<div class="date">NYC, February 22, 1951</div>
<table width="100%">
<tbody><tr><td width="15%">590</td><td>Don't You Know I Love You
</td></tr></tbody></table>
Willis Jackson (tenor saxophone) Harry Van Walls (piano) Connie Kay (drums) The Clovers (doo wop group) and others
<div class="date">NYC, December 19, 1951</div>
<table width="100%">
<tbody><tr><td width="15%">753</td><td>In The Middle Of The Night
</td></tr></tbody></table>
The Clovers (doo wop group)
<div class="date">NYC, March 18, 1952</div>
<table width="100%">
<tbody><tr><td width="15%">821</td><td>I Played The Fool
</td></tr><tr><td>822</td><td>Ting-A-Ling
</td></tr></tbody></table>
Bill Harris (guitar) John Bailey (lead vocals) Matthew McQuater (tenor vocals) Harold Lucas (baritone vocals) Harold Winley (bass vocals)
<div class="date">NYC, August 7, 1952</div>
<table width="100%">
<tbody><tr><td width="15%">872</td><td>Crawlin'
</td></tr><tr><td>873</td><td>Yes, It's You
</td></tr><tr><td>874</td><td>Hey, Miss Fannie
</td></tr></tbody></table>
The Clovers (doo wop group)
<div class="date">NYC, April 8, 1953</div>
<table width="100%">
<tbody><tr><td width="15%">1041</td><td>Here Goes A Fool
</td></tr></tbody></table>
same personnel
<div class="date">NYC, September 24, 1953</div>
<table width="100%">
<tbody><tr><td width="15%">1122</td><td>Lovey Dovey
</td></tr><tr><td>1123</td><td>I Got My Eyes On You
</td></tr><tr><td>1124</td><td>Little Mama
</td></tr></tbody></table>
same personnel
<div class="date">NYC, December 16, 1954</div>
<table width="100%">
<tbody><tr><td width="15%">1402</td><td>Blue Velvet
</td></tr></tbody></table>
same personnel
<div class="date">NYC, November 11, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1689</td><td>Devil Or Angel
</td></tr></tbody></table>
same personnel
<div class="date">NYC, March 29, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1940</td><td>Love, Love, Love
</td></tr></tbody></table>
** also issued on Atlantic LP 8009.
<h3><a name="1249">1249 &nbsp; Dave Pell - Love Story</a></h3>
Don Fagerquist (trumpet) Ray Sims (trombone) Dave Pell (tenor saxophone, bass clarinet, English horn) Marty Berman (baritone saxophone) Andre Previn (piano) Tony Rizzi (guitar) Mel Pollan (bass) Irv Kluger (drums)
<div class="date">Los Angeles, CA, February 13, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1888</td><td>Can't We Be Friends
</td></tr><tr><td>1889</td><td>I've Got A Crush On You
</td></tr><tr><td>1890</td><td>I've Got A Feeling I'm Falling
</td></tr><tr><td>1891</td><td>Love Is The Sweetest Thing
</td></tr></tbody></table>
Claude Williamson (piano) replaces Previn
<div class="date">Los Angeles, CA, February 20, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1892</td><td>Just One More Chance
</td></tr><tr><td>1893</td><td>If I Could Be With You One Hour Tonight
</td></tr><tr><td>1894</td><td>Who Walks In When I Walk Out
</td></tr><tr><td>1895</td><td>Let's Do It
</td></tr></tbody></table>
Andre Previn (piano) replaces Williamson
<div class="date">Los Angeles, CA, February 21, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1926</td><td>You Can't Pull The Wool Over My Eyes
</td></tr><tr><td>1927</td><td>Solitude
</td></tr><tr><td>1928</td><td>I've Found A New Baby
</td></tr><tr><td>1929</td><td>Bewitched, Bothered And Bewildered
</td></tr></tbody></table>
<h3><a name="1250">1250 &nbsp; Thomas Talbert - Bix, Duke, Fats</a></h3>
Nick Travis, Joe Wilder (trumpet) Eddie Bert, Jimmy Cleveland (trombone) Aaron Sachs (clarinet, tenor saxophone) George Wallington (piano) Oscar Pettiford (bass) Osie Johnson (drums) Tom Talbert (arranger, conductor)
<div class="date">NYC, August 24, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2092</td><td>Keepin' Out Of Mischief Now
</td></tr><tr><td>2093</td><td>Black And Blue
</td></tr><tr><td>2094</td><td>Clothesline Ballet
</td></tr><tr><td>2095</td><td>Bond Street
</td></tr></tbody></table>
Joe Wilder (trumpet) Jim Buffington (French horn) Joe Soldo (flute) Harold Goltzer (bassoon) Danny Bank (clarinet) Barry Galbraith (guitar) Oscar Pettiford (bass) Osie Johnson (drums) Tom Talbert (arranger, conductor)
<div class="date">NYC, September 7, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2135</td><td>Candlelights
</td></tr><tr><td>2136</td><td>In A Mist
</td></tr><tr><td>2137</td><td>In The Dark
</td></tr></tbody></table>
Joe Wilder (trumpet) Eddie Bert (trombone) Jim Buffington (French horn) Aaron Sachs (clarinet, tenor saxophone) Danny Bank (bass clarinet) Joe Soldo (alto saxophone, flute) Claude Williamson (piano) Barry Galbraith (guitar) Oscar Pettiford (bass) Osie Johnson (drums) Tom Talbert (arranger, conductor)
<div class="date">NYC, September 14, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2138</td><td>Prelude To A Kiss
</td></tr><tr><td>2139</td><td>Green Night And Orange Bright
</td></tr><tr><td>2140</td><td>Medley: Do Nothin' Till You Hear From Me / Koko
</td></tr></tbody></table>
** also issued on Atlantic SD 1250.
<h3><a name="1251">1251 &nbsp; Al Hibbler - After The Lights Go Down Low</a></h3>
Billy Kyle (piano) Al Hibbler (vocals) and others
<div class="date">NYC, April 19, 1950</div>
<table width="100%">
<tbody><tr><td width="15%">406</td><td>Dedicated To You
</td></tr><tr><td>409</td><td>If I Knew You Were There
</td></tr><tr><td>410</td><td>Song Of The Wanderer
</td></tr></tbody></table>
Al Hibbler (vocals) Billy Taylor, and others
<div class="date">NYC, October 25, 1950</div>
<table width="100%">
<tbody><tr><td width="15%">527</td><td>The Blues Came Falling Down
</td></tr><tr><td>529</td><td>I'm Travelin' Light
</td></tr></tbody></table>
Al Hibbler (vocals) Jimmy Mundy, and others
<div class="date">NYC, June 27, 1951</div>
<table width="100%">
<tbody><tr><td width="15%">613</td><td>Now I Lay Me Down To Dream
</td></tr><tr><td>614</td><td>This Is Always
</td></tr><tr><td>615</td><td>I Won't Tell A Soul
</td></tr></tbody></table>
omit Mundy
<div class="date">NYC, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">4449</td><td>After The Lights Go Down Low
</td></tr><tr><td>4450</td><td>You Will Be Mine
</td></tr><tr><td>4451</td><td>Tell Me
</td></tr><tr><td>4452</td><td>Autumn Winds
</td></tr></tbody></table>
<h3><a name="1252">1252 &nbsp; Alfred Ryder/Vernon Duke - This Is My Beloved</a></h3>
narration by Alfred Ryder, original music score by Vernon Duke. orchestra and chorus conducted by Lehman Engel.
<div class="date">NYC, January 22, 1949</div>
<table width="100%">
<tbody><tr><td width="15%"></td><td>"This Is My Beloved" Score
</td></tr></tbody></table>
<h3><a name="1253">1253 &nbsp; Wilbur DeParis At Symphony Hall</a></h3>
Sidney DeParis (trumpet) Wilbur DeParis (trombone) Omer Simeon (clarinet) Sonny White (piano) Lee Blair (banjo) Benny Moten (bass) Wilbert Kirk (drums, harmonica)
<div class="date">"Symphony Hall", Boston, MA, October 26, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2190</td><td>Majorca
</td></tr><tr><td>2191</td><td>Juba Dance
</td></tr><tr><td>2192</td><td>Toll Gate Blues
</td></tr><tr><td>2193</td><td>Wrought Iron Rag
</td></tr><tr><td>2194</td><td>Cielito Lindo
</td></tr><tr><td>2195</td><td>I Wish I Could Shimmy Like My Sister Kate
</td></tr><tr><td>2196</td><td>Banjoker
</td></tr><tr><td>2197</td><td>Piano Blues
</td></tr><tr><td>2198</td><td>Farewell Blues
</td></tr></tbody></table>
** also issued on Atlantic SD 1253.
<h3><a name="1254">1254 &nbsp; The Jimmy Giuffre 3</a></h3>
Jimmy Giuffre (clarinet, tenor, baritone saxophone) Jim Hall (guitar) Ralph Pena (bass)
<div class="date">Capitol Studios, Hollywood, CA, December 3, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2282</td><td>Gotta Dance
</td></tr><tr><td>2284</td><td>The Train And The River
</td></tr><tr><td>2285</td><td>The Song Is You
</td></tr><tr><td>2286</td><td>That's The Way It Is
</td></tr></tbody></table>
same personnel
<div class="date">Capitol Studios, Hollywood, CA, December 4, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2287</td><td>Two Kinds Of Blues
</td></tr><tr><td>2288</td><td>Crazy She Calls Me
</td></tr><tr><td>2289</td><td>My All
</td></tr><tr><td>2290</td><td>Crawdad Suite
</td></tr><tr><td>2283</td><td>Voodoo
</td></tr></tbody></table>
** also issued on Atlantic 7567-90981-2.<br>
** part of Mosaic MQ10-176, MD6-176.
<h3><a name="1255">1255 &nbsp; Joe Mooney - Lush Life</a></h3>
Joe Mooney (organ, vocals) Lonesome Jimmie Lee Robinson (guitar) Milt Hinton (bass) Osie Johnson (drums)
<div class="date">NYC, November 28, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2632</td><td>Lush Life
</td></tr><tr><td>2633</td><td>The Kid's A Dreamer
</td></tr><tr><td>2634</td><td>My One And Only Love
</td></tr><tr><td>2635</td><td>That's All
</td></tr></tbody></table>
same personnel
<div class="date">NYC, November 29, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2636</td><td>Nina Never Knew
</td></tr><tr><td>2637</td><td>Love Is Here To Stay
</td></tr><tr><td>2638</td><td>Polka Dots And Moonbeams
</td></tr><tr><td>2639</td><td>Nowhere
</td></tr><tr><td>2640</td><td>Have You Met Miss Jones
</td></tr></tbody></table>
same personnel
<div class="date">NYC, November 30, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2641</td><td>Crazy She Calls Me
</td></tr></tbody></table>
<h3><a name="1256">1256 &nbsp; Carol Stevens And Phil Moore's Music</a></h3>
Nick Travis (trumpet) Don Elliott (trumpet, mellophone) Warren Covington or Eddie Bert (trombone) Herbie Mann (alto flute) Phil Bodner (English horn, clarinet) Sol Schlinger (bass clarinet) Bernie Kaufman (bass clarinet, flute) Romeo Penque (woodwinds) Bobby Rosengarden (vibraphone) Frank Berry, Phil Moore (piano) Barry Galbraith (guitar) Milt Hinton (bass) Osie Johnson (drums) Phil Kraus (percussion) Carol Stevens (vocals)
<div class="date">NYC, February 19, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2394</td><td>Lyin' In The Hay
</td></tr><tr><td>2395</td><td>In A Mellotone
</td></tr><tr><td>2396</td><td>Tender As A Rose
</td></tr><tr><td>2397</td><td>Saved It All For Me
</td></tr></tbody></table>
same personnel
<div class="date">NYC, March 11, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2398</td><td>Mood For You
</td></tr><tr><td>2399</td><td>At Last
</td></tr><tr><td>2400</td><td>Romance In The Dark
</td></tr><tr><td>2401</td><td>Everywhere
</td></tr></tbody></table>
same personnel
<div class="date">NYC, March 13, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2402</td><td>I'm Playing With Fire
</td></tr><tr><td>2403</td><td>Satin Doll
</td></tr><tr><td>2404</td><td>Lurelei (F.H.C.)
</td></tr><tr><td>2405</td><td>Keep On Doin' What You're Doin'
</td></tr></tbody></table>
<h3><a name="1257">1257 &nbsp; Dizzy Gillespie - Dizzy At Home And Abroad</a></h3>
Dizzy Gillespie (trumpet) Bill Graham (alto, baritone saxophone) Milt Jackson (vibraphone, piano) Percy Heath (bass) Al Jones (drums) Joe Carroll (vocals -1,4)
<div class="date">NYC, February 29, 1952</div>
<table width="100%">
<tbody><tr><td width="15%">1. 805</td><td>Groovin' The Nursery Rhymes
</td></tr><tr><td>2. 806</td><td>This Is Happiness
</td></tr><tr><td>3. 807</td><td>Dizz' Tune (Mrs. Diz)
</td></tr><tr><td>4. 808</td><td>Love Is Here To Stay
</td></tr></tbody></table>
Dizzy Gillespie (trumpet, vocals) Don Byas (tenor saxophone) Art Simmons (piano) Joe Benjamin (bass) Bill Clark (drums) Humberto Morales (congas)
<div class="date">"Theatre Des Champs-Elysees", Paris, France, March 25, 1952</div>
<table width="100%">
<tbody><tr><td width="15%">14776 | 875</td><td>Cocktails For Two
</td></tr><tr><td>14777 | 877</td><td>Cognac Blues
</td></tr><tr><td>14780 | 941</td><td>Blue And Sentimental
</td></tr></tbody></table>
Dizzy Gillespie (trumpet, vocals) Don Byas (tenor saxophone) Arnold Ross (piano) Joe Benjamin (bass) Bill Clark (drums)
<div class="date">"Theatre Des Champs-Elysees", Paris, France, April 6, 1952</div>
<table width="100%">
<tbody><tr><td width="15%">15173 | 943</td><td>When It's Sleepy Time Down South
</td></tr><tr><td>15174 | 939</td><td>Lullaby In Rhythm
</td></tr><tr><td>15175 | 945</td><td>Just Blues (One More Blues)
</td></tr><tr><td>15177 | 944</td><td>Ain't Misbehavin'
</td></tr><tr><td>15180 | 938</td><td>Mama's Blues (Blues Chante) (Mrs. Dizzy Blues)
</td></tr></tbody></table>
<h3><a name="1258">1258 &nbsp; Lee Konitz - Inside Hi-Fi</a></h3>
Lee Konitz (alto, tenor saxophone) Sal Mosca (piano) Peter Ind (bass) Dick Scott (drums)
<div class="date">NYC, September 26, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2247-3</td><td>Indiana
</td></tr><tr><td>2249-2</td><td>Star Eyes
</td></tr><tr><td>2250-1</td><td>Nesuhi's Instant
</td></tr><tr><td>2252-4</td><td>All Of Me
</td></tr></tbody></table>
Lee Konitz (alto, tenor saxophone) Billy Bauer (guitar) Arnold Fishkin (bass) Dick Scott (drums)
<div class="date">NYC, October 16, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2256-2</td><td>Sweet And Lovely
</td></tr><tr><td>2257-4</td><td>Cork 'N' Bib (Cork 'N' Rib)
</td></tr><tr><td>2258-3</td><td>Everything Happens To Me
</td></tr><tr><td>2259-1</td><td>Kary's Trance
</td></tr></tbody></table>
** also issued on Atlantic SD 1258.
<h3><a name="1259">1259 &nbsp; The Great Ray Charles</a></h3>
Ray Charles (piano, vocals) Oscar Pettiford (bass) Joe Harris (drums)
<div class="date">NYC, April 30, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1968</td><td>Black Coffee
</td></tr></tbody></table>
Joe Bridgewater, John Hunt (trumpet) David Newman (tenor, alto saxophone) Emmett Dennis (baritone saxophone) Ray Charles (piano, vocals) Roosevelt Sheffield (bass) William Peeples (drums)
<div class="date">NYC, November 20, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2223</td><td>The Ray
</td></tr><tr><td>2224</td><td>I Surrender, Dear
</td></tr><tr><td>2228A</td><td>Sweet Sixteen Bars
</td></tr></tbody></table>
same personnel
<div class="date">NYC, November 26, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2227</td><td>Doodlin'
</td></tr><tr><td>2228</td><td>There's No You
</td></tr><tr><td>2229</td><td>Undecided
</td></tr><tr><td>2230</td><td>My Melancholy Baby
</td></tr></tbody></table>
** also issued on Atlantic SD 1259.
<h3><a name="1260">1260 &nbsp; Charles Mingus - The Clown</a></h3>
Jimmy Knepper (trombone) Curtis Porter (tenor saxophone) Wade Legge (piano) Charles Mingus (bass) Dannie Richmond (drums) Jean Shepherd (narrator)
<div class="date">Audio-Video Studios, NYC, February 12, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2452</td><td>The Clown
</td></tr></tbody></table>
Jimmy Knepper (trombone) Curtis Porter (alto saxophone) Wade Legge (piano) Charles Mingus (bass) Dannie Richmond (drums)
<div class="date">NYC, March 13, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2455</td><td>Blue Cee
</td></tr><tr><td>2457</td><td>Reincarnation Of A Love Bird
</td></tr><tr><td>2458</td><td>Haitian Fight Song
</td></tr></tbody></table>
** part of Rhino R2 72871.
<h3><a name="1261">1261 &nbsp; Dixieland At Jazz Ltd.</a></h3>
Munn Ware (trombone) Bill Reinhardt (clarinet) Sidney Bechet (soprano saxophone) Don Ewell (piano) Sid Thall (bass) Wally Gordon (drums)
<div class="date">Chicago, IL, February 12, 1949</div>
<table width="100%">
<tbody><tr><td width="15%">UB9101 | 934</td><td>Maryland, My Maryland
</td></tr><tr><td>UB9102 | 931</td><td>Careless Love
</td></tr><tr><td>UB9103 | 936</td><td>Egyptian Fantasy
</td></tr></tbody></table>
Don Ewell (piano) Sid Thall (bass) Wally Gordon (drums)
<div class="date"></div>
<table width="100%">
<tbody><tr><td width="15%">UB9104 | 933</td><td>Maple Leaf Rag
</td></tr></tbody></table>
add Doc Evans (cornet) Munn Ware (trombone) Bill Reinhardt (clarinet)
<div class="date">Chicago, IL, February, 1949</div>
<table width="100%">
<tbody><tr><td width="15%">UB9181 | 937</td><td>Wolverine Blues
</td></tr><tr><td>UB9182 | 932</td><td>It's A Long Way To Tipperary
</td></tr></tbody></table>
Muggsy Spanier (cornet) replaces Evans
<div class="date"></div>
<table width="100%">
<tbody><tr><td width="15%">UB9183 | 935</td><td>A Good Man Is Hard To Find
</td></tr><tr><td>UB9184 | 930</td><td>Washington And Lee Swing
</td></tr></tbody></table>
Doc Evans (cornet) Miff Mole (trombone) Bill Reinhardt (clarinet) Ralph Blank (piano) Sy Nelson (bass) Doc Cenardo (drums)
<div class="date">Chicago, IL, 1949</div>
<table width="100%">
<tbody><tr><td width="15%">946</td><td>Jazz Me Blues
</td></tr><tr><td>947</td><td>The Charleston
</td></tr><tr><td>948</td><td>Tin Roof Blues
</td></tr><tr><td>949</td><td>High Society
</td></tr></tbody></table>
<h3><a name="1262">1262 &nbsp; Bobby Short - Speaking Of Love</a></h3>
Bobby Short (piano, vocals) Ismael Ugarte (bass) Ramon "Sonny" Rivera (drums)
<div class="date">NYC, November 29, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2235A</td><td>So Near And Yet So Far
</td></tr><tr><td>2236</td><td>At Long Last Love
</td></tr><tr><td>2237</td><td>I've Got Beginner's Luck
</td></tr><tr><td>2238</td><td>Let's Fall In Love
</td></tr><tr><td>2239</td><td>Do I Hear You Saying I Love You
</td></tr><tr><td>2240</td><td>Easy Come, Easy Go
</td></tr><tr><td>2241</td><td>I Love You, Samantha
</td></tr><tr><td>2242</td><td>Hooray For Love
</td></tr></tbody></table>
same personnel
<div class="date">NYC, January 10, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2471</td><td>I Fall In Love With You Every Day
</td></tr><tr><td>2472</td><td>Down In Mexico
</td></tr><tr><td>2473</td><td>That's What I Call Love
</td></tr><tr><td>2474</td><td>Year After Year
</td></tr><tr><td>2475</td><td>Speaking Of Love
</td></tr><tr><td>2476</td><td>I Wanna Be Loved
</td></tr></tbody></table>
** also issued on Atlantic SD 1262.
<h3><a name="1263">1263 &nbsp; The Warm Sound Of Frances Wayne</a></h3>
Jerome Richardson (flute, baritone saxophone) Billy Rowland (piano) Billy Mure (guitar) Milt Hinton (bass) Osie Johnson (drums) Frances Wayne (vocals)
<div class="date">NYC, April 4, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2406</td><td>Two For The Blues
</td></tr><tr><td>2407</td><td>Caravan
</td></tr><tr><td>2408</td><td>Early Autumn
</td></tr><tr><td>2409</td><td>Soft Winds
</td></tr></tbody></table>
Urbie Green (trombone) replaces Richardson
<div class="date">NYC, April 5, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2410</td><td>Prelude To A Kiss
</td></tr><tr><td>2411</td><td>A Smo-O-Oth One
</td></tr><tr><td>2412</td><td>Poor Little Buttercup
</td></tr><tr><td>2413</td><td>Blue And Sentimental
</td></tr></tbody></table>
Billy Butterfield (trumpet) replaces Green
<div class="date">NYC, April 6, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2416</td><td>'Round Midnight
</td></tr><tr><td>2417</td><td>Oh, What A Night For Love
</td></tr></tbody></table>
Al Cohn (tenor saxophone) Hank Jones (piano) Wendell Marshall (bass) Don Lamond (drums) Frances Wayne (vocals)
<div class="date">NYC, April 27, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2477</td><td>In Other Words
</td></tr><tr><td>2479</td><td>My One And Only Love
</td></tr><tr><td>2480</td><td>Speak Low
</td></tr><tr><td>2481</td><td>You Go To My Head
</td></tr></tbody></table>
<h3><a name="1264">1264 &nbsp; Joe Castro - Mood Jazz</a></h3>
Joe Castro (piano) Ed Shonk (bass) Philly Joe Jones (drums)
<div class="date">NYC, November 19, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2215</td><td>You Stepped Out Of A Dream
</td></tr></tbody></table>
John Hannan (trumpet) Glenn Prescott (alto saxophone) Joe Castro (piano) Ed Shonk (bass) Gus Johnson (drums) unidentified chorus, unidentified strings, Neal Hefti (arranger, conductor)
<div class="date">NYC, January 30, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2390</td><td>If You Could See Me Now
</td></tr><tr><td>2391</td><td>Without You
</td></tr><tr><td>2392</td><td>Angel Eyes
</td></tr><tr><td>2393</td><td>Caravan
</td></tr></tbody></table>
same personnel
<div class="date">NYC, February 2, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2330</td><td>J.C. Blues
</td></tr><tr><td>2331</td><td>Everything I Love
</td></tr><tr><td>2332</td><td>Doodlin'
</td></tr><tr><td>2333</td><td>It's You Or No One
</td></tr></tbody></table>
** also issued on Atlantic SD 1264.
<h3><a name="1265">1265 &nbsp; The Modern Jazz Quartet</a></h3>
Milt Jackson (vibraphone) John Lewis (piano) Percy Heath (bass) Connie Kay (drums)
<div class="date">NYC, April 5, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2501</td><td>Between The Devil And The Deep Blue Sea
</td></tr><tr><td>2502</td><td>La Ronde: Drums
</td></tr><tr><td>2503</td><td>A Night In Tunisia
</td></tr><tr><td>2504</td><td>Yesterdays
</td></tr><tr><td>2505</td><td>Bags' Groove
</td></tr><tr><td>2506</td><td>Baden-Baden
</td></tr><tr><td>2507</td><td>Ballad Medley: They Say It's Wonderful / How Deep Is The Ocean / (I Don't Stand) A Ghost Of A Chance With You / My Old Flame / Body And Soul
</td></tr></tbody></table>
<h3><a name="1266">1266 &nbsp; Jimmy Witherspoon And Wilbur DeParis "New" New Orleans Band - Callin' The Blues</a></h3>
Sidney DeParis (cornet) Wilbur DeParis (trombone) Omer Simeon (clarinet) Sonny White (piano) Shep Shepard (banjo) Benny Moten (bass) Wilbert Kirk (drums) Jimmy Witherspoon (vocals)
<div class="date">NYC, October 23, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2173 | A152</td><td>Ain't Nobody's Business
</td></tr><tr><td>2174 | A153</td><td>How Long Blues
</td></tr><tr><td>2176 | A155</td><td>St. Louis Blues
</td></tr></tbody></table>
same personnel
<div class="date">NYC, November 19, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2208 | A165</td><td>Lotus Blossom
</td></tr><tr><td>2209 | A166</td><td>When The Sun Goes Down
</td></tr><tr><td>2210 | A167</td><td>See See Rider
</td></tr><tr><td>2211 | A168</td><td>Careless Love
</td></tr><tr><td>2212 | A169</td><td>Trouble In Mind
</td></tr><tr><td>2213 | A170</td><td>Big Fine Girl
</td></tr><tr><td>2214 | A171</td><td>Good Rollin' Blues
</td></tr></tbody></table>
<h3><a name="1267">1267 &nbsp; John Lewis/Sacha Distel - Afternoon In Paris</a></h3>
Barney Wilen (tenor saxophone) John Lewis (piano) Sacha Distel (guitar) Percy Heath (bass) Kenny Clarke (drums)
<div class="date">Paris, France, December 4, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">4668</td><td>All The Things You Are
</td></tr><tr><td>4669</td><td>Bags' Groove
</td></tr><tr><td>4670</td><td>Willow Weep For Me
</td></tr></tbody></table>
Barney Wilen (tenor saxophone) John Lewis (piano) Sacha Distel (guitar) Pierre Michelot (bass) Connie Kay (drums)
<div class="date">Paris, France, December 7, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">4665</td><td>I Cover The Waterfront
</td></tr><tr><td>4666</td><td>Dear Old Stockholm
</td></tr><tr><td>4667</td><td>Afternoon In Paris
</td></tr></tbody></table>
<h3><a name="1268">1268 &nbsp; Conte Candoli/Lou Levy - West Coast Wailers</a></h3>
Conte Candoli (trumpet) Bill Holman (tenor saxophone) Lou Levy (piano) Leroy Vinnegar (bass) Lawrence Marable (drums)
<div class="date">Los Angeles, CA, August 16, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1713</td><td>Cheremoya
</td></tr><tr><td>1714</td><td>Marcia Lee
</td></tr></tbody></table>
same personnel
<div class="date">Los Angeles, CA, August 17, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1715</td><td>Pete's Alibi
</td></tr><tr><td>1716</td><td>Flamingo
</td></tr><tr><td>1717</td><td>Jordu
</td></tr><tr><td>1718</td><td>Comes Love
</td></tr><tr><td>1719</td><td>Lover Man
</td></tr><tr><td>1720</td><td>Lover Come Back To Me
</td></tr></tbody></table>
<h3><a name="1269">1269 &nbsp; Milt Jackson - Plenty, Plenty Soul</a></h3>
Joe Newman (trumpet) Lucky Thompson (tenor saxophone) Milt Jackson (vibraphone) Horace Silver (piano) Oscar Pettiford (bass) Connie Kay (drums)
<div class="date">NYC, January 5, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2435</td><td>Ignunt Oil
</td></tr><tr><td>2436</td><td>Blues At Twilight
</td></tr><tr><td>2437</td><td>Sermonette
</td></tr><tr><td>2438</td><td>The Spirit-Feel
</td></tr></tbody></table>
Joe Newman (trumpet) Jimmy Cleveland (trombone) Cannonball Adderley as Ronnie Peters (alto saxophone) Frank Foster (tenor saxophone) Sahib Shihab (baritone saxophone) Milt Jackson (vibraphone) Horace Silver (piano) Percy Heath (bass) Art Blakey (drums) Quincy Jones (arranger)
<div class="date">NYC, January 7, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2439</td><td>Plenty, Plenty Soul
</td></tr><tr><td>2440</td><td>Boogity Boogity
</td></tr><tr><td>2441</td><td>Heartstrings
</td></tr></tbody></table>
** also issued on Atlantic SD 1269, SD 8811.
<h3><a name="1270">1270 &nbsp; Shorty Rogers - Way Up There</a></h3>
Shorty Rogers (trumpet) Jimmy Giuffre (clarinet, tenor, baritone saxophone) Pete Jolly (piano) Curtis Counce (bass) Shelly Manne (drums)
<div class="date">Los Angeles, CA, March 3, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1733</td><td>Solarization
</td></tr></tbody></table>
Shorty Rogers (trumpet, flugelhorn) Jimmy Giuffre (clarinet, tenor, baritone saxophone) Lou Levy (piano) Ralph Pena (bass) Shelly Manne (drums)
<div class="date">Los Angeles, CA, October 26, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1744</td><td>March Of The Martians
</td></tr></tbody></table>
Conte Candoli, Pete Candoli, Harry Edison, Don Fagerquist (trumpet) Shorty Rogers (trumpet, flugelhorn) Lou Levy (piano) Ralph Pena (bass) Shelly Manne (drums)
<div class="date">Los Angeles, CA, December 6, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1773</td><td>Pixieland
</td></tr></tbody></table>
Shorty Rogers (trumpet, flugelhorn) Bob Enevoldsen (valve trombone) John Graas (French horn) Paul Sarmento (tuba) Jimmy Giuffre (clarinet, tenor, baritone saxophone) Bud Shank (alto saxophone) Lou Levy (piano) Ralph Pena (bass) Shelly Manne (drums)
<div class="date">Los Angeles, CA, December 9, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1775</td><td>Wail Of Two Cities
</td></tr></tbody></table>
Harry Edison (trumpet) Shorty Rogers (trumpet, flugelhorn) Bud Shank (alto saxophone) Pete Jolly (piano) Barney Kessel (guitar) Leroy Vinnegar (bass) Shelly Manne (drums)
<div class="date">Los Angeles, CA, December 16, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">1789</td><td>Blues Way Up There
</td></tr><tr><td>1790</td><td>Blues Way Down There
</td></tr></tbody></table>
<h3><a name="1271">1271 &nbsp; Mary Lou Williams/Barbara Carroll - Ladies Of Jazz</a></h3>
Mary Lou Williams (piano) Carl Pruitt (bass) Bill Clark (drums)
<div class="date">NYC, March 7, 1951</div>
<table width="100%">
<tbody><tr><td width="15%">582</td><td>Opus Z (Stennell)
</td></tr><tr><td>583</td><td>The Surrey With The Fringe On Top
</td></tr><tr><td>585</td><td>Pagliacci
</td></tr><tr><td>586</td><td>'S Wonderful
</td></tr><tr><td>587</td><td>From This Moment On
</td></tr><tr><td>588</td><td>You're The Cream In My Coffee
</td></tr><tr><td>591</td><td>In The Purple Grotto
</td></tr></tbody></table>
Barbara Carroll (piano, vocals) probably Danny Martucci (bass) Herbie Wasserman (drums)
<div class="date">NYC, November 9, 1951</div>
<table width="100%">
<tbody><tr><td width="15%">669</td><td>Love Of My Life
</td></tr><tr><td>671</td><td>'Tis Autumn
</td></tr><tr><td>672</td><td>Takin' A Chance On Love
</td></tr><tr><td>673</td><td>The Lady's In Love With You
</td></tr><tr><td>674</td><td>Autumn In New York
</td></tr><tr><td>675</td><td>You Took Advantage Of Me
</td></tr><tr><td>676</td><td>My Funny Valentine
</td></tr></tbody></table>
<h3><a name="1272">1272 &nbsp; The John Lewis Piano</a></h3>
John Lewis (piano) Barry Galbraith (guitar) Percy Heath (bass) Connie Kay (drums)
<div class="date">NYC, July 30, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2527</td><td>It Never Entered My Mind
</td></tr><tr><td>2528</td><td>The Bad And The Beautiful
</td></tr><tr><td>2529</td><td>Warmeland (Dear Old Stockholm)
</td></tr></tbody></table>
omit Galbraith
<div class="date">NYC, February 21, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2459</td><td>Little Girl Blue
</td></tr><tr><td>2460</td><td>D&amp;E
</td></tr></tbody></table>
John Lewis (piano) Jim Hall (guitar) Connie Kay (drums)
<div class="date">"Music Inn", Lenox, MA, August 24, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2714</td><td>Original, No. 1 (Pierrot)
</td></tr><tr><td>2720</td><td>Original, No. 2 (Colombine)
</td></tr><tr><td>2721</td><td>Original, No. 3 (Harlequin)
</td></tr></tbody></table>
<h3><a name="1273">1273 &nbsp; The Real Lee Konitz</a></h3>
Don Ferrara (trumpet -5,6) Lee Konitz (alto saxophone) Billy Bauer (guitar) Peter Ind (bass) Dick Scott (drums)
<div class="date">"Midway Lounge", Pittsburgh, PA, February 15, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">1. 2566</td><td>All Of Me (Straight Away)
</td></tr><tr><td>2. 2567</td><td>Foolin' Myself
</td></tr><tr><td>3. 2568</td><td>You Go To My Head
</td></tr><tr><td>4. 2569</td><td>My Melancholy Baby
</td></tr><tr><td>5. 2570</td><td>Pennies In Minor
</td></tr><tr><td>6. 2571</td><td>Sweet And Lovely
</td></tr><tr><td>7. 2572</td><td>Easy Living
</td></tr><tr><td>8. 2573</td><td>Indiana (Midway)
</td></tr></tbody></table>
<h3><a name="1274">1274 &nbsp; Teddy Charles - The Word From Bird</a></h3>
Art Farmer (trumpet) Eddie Bert (trombone -1) Jim Buffington (French horn -1) Don Butterfield (tuba) Hal Stein (alto saxophone) Bob Newman (tenor saxophone) George Barrow (baritone saxophone) Teddy Charles (vibraphone) Hall Overton (piano) Jimmy Raney (guitar) Addison Farmer (bass) Ed Shaughnessy (drums)
<div class="date">NYC, October 23, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">1. 2199</td><td>A Word From Bird
</td></tr><tr><td>2. 2200</td><td>Showtime
</td></tr></tbody></table>
Teddy Charles (vibraphone) Hall Overton (piano) Charles Mingus (bass) Ed Shaughnessy (drums)
<div class="date">NYC, November 12, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2188</td><td>Laura
</td></tr><tr><td>2201</td><td>When Your Lover Has Gone
</td></tr><tr><td>2202</td><td>Just One Of Those Things
</td></tr><tr><td>2203</td><td>Blue Greens
</td></tr></tbody></table>
<h3><a name="1275">1275 &nbsp; George Wallington - Knight Music</a></h3>
George Wallington (piano) Teddy Kotick (bass) Nick Stabulas (drums)
<div class="date">NYC, September 4 &amp; 5, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2142</td><td>Godchild
</td></tr><tr><td>2143</td><td>In A Sentimental Mood
</td></tr><tr><td>2144</td><td>The End Of A Love Affair
</td></tr><tr><td>2145</td><td>Will You Still Be Mine
</td></tr><tr><td>2146</td><td>Billie's Tune
</td></tr><tr><td>2147</td><td>The Ghostly Lover
</td></tr><tr><td>2148</td><td>Up Jumped The Devil
</td></tr><tr><td>2149</td><td>World Weary
</td></tr><tr><td>2150</td><td>Serendipity
</td></tr><tr><td>2151</td><td>It's All Right With Me
</td></tr><tr><td>2153</td><td>One Night Of Love
</td></tr></tbody></table>
** also issued on Atlantic SD 1275.
<h3><a name="1276">1276 &nbsp; Jimmy Giuffre And His Music Men Play "The Music Man"</a></h3>
Bernie Glow, Phil Sunkel, Joe Wilder (trumpet) Jimmy Giuffre (clarinet, tenor, baritone saxophone) Al Cohn, Eddie Wasserman (tenor saxophone) Sol Schlinger (baritone saxophone) Wendell Marshall (bass) Ed Shaughnessy (drums)
<div class="date">Coastal Recording Studios, NYC, December 31, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2887</td><td>Marian The Librarian
</td></tr><tr><td>2888</td><td>Seventy-Six Trombones
</td></tr></tbody></table>
same personnel
<div class="date">Coastal Recording Studios, NYC, January 2, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">2889</td><td>Goodnight My Someone
</td></tr><tr><td>2890</td><td>My White Knight
</td></tr><tr><td>2891</td><td>'Till There Was You
</td></tr></tbody></table>
Nick Travis (trumpet) replaces Glow
<div class="date">Coastal Recording Studios, NYC, January 3, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">2892</td><td>It's You
</td></tr><tr><td>2893</td><td>Ship Ahoy! (Shipoopi)
</td></tr><tr><td>2894</td><td>Wells Fargo Wagon
</td></tr></tbody></table>
Art Farmer, Bernie Glow (trumpet) replaces Travis, Wilder
<div class="date">Coastal Recording Studios, NYC, January 6, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">2895</td><td>Iowa Stubborn
</td></tr><tr><td>2896</td><td>Gary, Indiana
</td></tr><tr><td>2897</td><td>Lida Rose (Will I Ever Tell You)
</td></tr></tbody></table>
** also issued on Atlantic SD 1276.<br>
** part of Mosaic MQ10-176, MD6-176.
<h3><a name="1277">1277 &nbsp; The Billy Taylor Touch</a></h3>
Billy Taylor (piano) John Collins (guitar) Al Hall (bass) Shadow Wilson (drums)
<div class="date">NYC, February 20, 1951</div>
<table width="100%">
<tbody><tr><td width="15%">561</td><td>Wrap Your Troubles In Dreams
</td></tr><tr><td>562</td><td>Thou Swell
</td></tr><tr><td>563</td><td>Good Groove
</td></tr><tr><td>564</td><td>Somebody Loves Me
</td></tr><tr><td>565</td><td>Willow Weep For Me
</td></tr><tr><td>566</td><td>If I Had You
</td></tr><tr><td>567</td><td>The Very Thought Of You
</td></tr><tr><td>568</td><td>What Is There To Say
</td></tr></tbody></table>
Billy Taylor (piano) Earl May (bass) Ed Thigpen (drums)
<div class="date">NYC, October 28, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2783</td><td>You Make Me Feel So Young
</td></tr><tr><td>2784</td><td>Early May
</td></tr><tr><td>2785</td><td>I Get A Kick Out Of You
</td></tr><tr><td>2786</td><td>Can You Tell By Looking At Me
</td></tr></tbody></table>
<h3><a name="1278">1278 &nbsp; Art Blakey's Jazz Messengers With Thelonious Monk - Jazz Connection</a></h3>
Bill Hardman (trumpet) Johnny Griffin (tenor saxophone) Thelonious Monk (piano) Spanky DeBrest (bass) Art Blakey (drums)
<div class="date">NYC, May 14, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2560</td><td>Blue Monk
</td></tr><tr><td>2561</td><td>I Mean You
</td></tr></tbody></table>
same personnel
<div class="date">NYC, May 15, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2562</td><td>Rhythm-A-Ning
</td></tr><tr><td>2563</td><td>Purple Shades
</td></tr><tr><td>2564</td><td>Evidence
</td></tr><tr><td>2565</td><td>In Walked Bud
</td></tr></tbody></table>
** also issued on Atlantic SD 1278.
<h3><a name="1279">1279 &nbsp; Milt Jackson/Ray Charles - Soul Brothers</a></h3>
Ray Charles (alto saxophone, piano) Billy Mitchell (tenor saxophone) Milt Jackson (vibraphone, piano, guitar) Skeeter Best (guitar -1,2,4,5) Oscar Pettiford (bass) Connie Kay (drums)
<div class="date">NYC, September 12, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">1. 2726</td><td>How Long, How Long Blues
</td></tr><tr><td>2. 2727</td><td>Cosmic Ray
</td></tr><tr><td>3. 2732</td><td>'Deed I Do
</td></tr><tr><td>4. 2733</td><td>Blue Funk
</td></tr><tr><td>5. 2734</td><td>Soul Brothers
</td></tr><tr><td>6. 2735</td><td>Bags Guitar Blues
</td></tr></tbody></table>
** also issued on Atlantic SD 1279.
<h3><a name="1280">1280 &nbsp; The Jazz Modes - The Most Happy Fella</a></h3>
Julius Watkins (French horn) Charlie Rouse (tenor saxophone) Gildo Mahones (piano) Martin Rivera (bass) Ron Jefferson (drums) Chino Pozo (congas, bongos)
<div class="date">NYC, November 7, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2810</td><td>Like A Woman
</td></tr><tr><td>2811</td><td>Joey, Joey, Joey
</td></tr><tr><td>2812</td><td>Warm All Over
</td></tr><tr><td>2813</td><td>Somebody Somewhere
</td></tr></tbody></table>
Julius Watkins (French horn) Charlie Rouse (tenor saxophone) Gildo Mahones (piano) Martin Rivera (bass) Ron Jefferson (drums) Chino Pozo (congas, bongos) Eileen Gilbert (voice -2)
<div class="date">NYC, November 11, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">1. 2826</td><td>Standing On The Corner
</td></tr><tr><td>2. 2827</td><td>My Heart Is So Full Of You
</td></tr><tr><td>3. 2828</td><td>The Most Happy Fella
</td></tr><tr><td>4. 2829</td><td>Don't Cry
</td></tr><tr><td>5. 2830</td><td>Happy To Make Your Acquaintance
</td></tr></tbody></table>
<h3><a name="1281">1281 &nbsp; LaVern Baker Sings Bessie Smith</a></h3>
Buck Clayton (trumpet) Vic Dickenson (trombone) Paul Quinichette (tenor saxophone) Sahib Shihab (baritone saxophone) Nat Pierce (piano) Danny Barker (guitar) Wendell Marshall (bass) Joe Marshall (drums) LaVern Baker (vocals) Phil Moore (arranger)
<div class="date">NYC, January 27, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">2935</td><td>Nobody Knows You When You're Down And Out
</td></tr><tr><td>2936</td><td>Gimme A Pigfoot
</td></tr><tr><td>2937</td><td>Baby Doll
</td></tr><tr><td>2938</td><td>On Revival Day
</td></tr></tbody></table>
Buck Clayton (trumpet) Jimmy Cleveland (trombone) Paul Quinichette (tenor saxophone) Sahib Shihab (baritone saxophone) Nat Pierce (piano) Danny Barker (guitar) Wendell Marshall (bass) Joe Marshall (drums) LaVern Baker (vocals) Phil Moore, Nat Pierce, Ernie Wilkins (arranger)
<div class="date">NYC, January 28, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">2939</td><td>Money Blues
</td></tr><tr><td>2940</td><td>Empty Bedroom Blues
</td></tr><tr><td>2941</td><td>I Ain't Gonna Play No Second Fiddle
</td></tr><tr><td>2942</td><td>There'll Be A Hot Time In The Old Town Tonight
</td></tr></tbody></table>
Urbie Green (trombone) Jerome Richardson (baritone saxophone) replaces Cleveland, Shihab
<div class="date">NYC, January 29, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">2943</td><td>Back Water Blues
</td></tr><tr><td>2944</td><td>After You've Gone
</td></tr><tr><td>2945</td><td>Young Woman's Blues
</td></tr><tr><td>2946</td><td>Preaching Blues
</td></tr></tbody></table>
** also issued on Atlantic SD 1281.
<h3><a name="1282">1282 &nbsp; The Jimmy Giuffre 3 - Trav'lin' Light</a></h3>
Bob Brookmeyer (valve trombone) Jimmy Giuffre (clarinet, tenor, baritone saxophone) Jim Hall (guitar)
<div class="date">Atlantic Studios, NYC, January 20, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">2913</td><td>Pickin' 'Em Up And Layin' 'Em Down
</td></tr><tr><td>2914</td><td>The Green Country (New England Mood)
</td></tr></tbody></table>
same personnel
<div class="date">Atlantic Studios, NYC, January 21, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">2916</td><td>The Lonely Time
</td></tr><tr><td>2917</td><td>Trav'lin' Light
</td></tr><tr><td>2918</td><td>Forty-Second Street
</td></tr></tbody></table>
same personnel
<div class="date">Atlantic Studios, NYC, January 23, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">2932</td><td>Show Me The Way To Go Home
</td></tr><tr><td>2933</td><td>The Swamp People
</td></tr><tr><td>2934</td><td>California, Here I Come
</td></tr></tbody></table>
** part of Mosaic MQ10-176, MD6-176.
<h3><a name="1283">1283 &nbsp; Jimmy And Mama Yancey - Pure Blues</a></h3>
Jimmy Yancey (piano) Israel Crosby (bass)
<div class="date">Chicago, IL, July 18, 1951</div>
<table width="100%">
<tbody><tr><td width="15%">727</td><td>Mournful Blues
</td></tr><tr><td>728</td><td>Salute To Pinetop
</td></tr><tr><td>729</td><td>35th And Dearborn
</td></tr><tr><td>730</td><td>How Long Blues
</td></tr></tbody></table>
same session
<div class="date"></div>
<table width="100%">
<tbody><tr><td width="15%">736 (2nd)</td><td>Yancey Special (2nd version)
</td></tr></tbody></table>
add Mama Yancey (vocals)
<div class="date"></div>
<table width="100%">
<tbody><tr><td width="15%">738</td><td>Santa Fe Blues
</td></tr><tr><td>739</td><td>How Long Blues
</td></tr><tr><td>740</td><td>Four O'Clock Blues
</td></tr><tr><td>741</td><td>Make Me A Pallet On The Floor
</td></tr><tr><td>742</td><td>Monkey Woman Blues
</td></tr></tbody></table>
omit Mama Yancey
<div class="date"></div>
<table width="100%">
<tbody><tr><td width="15%">743</td><td>Yancey's Bugle Call
</td></tr><tr><td>744</td><td>Shave 'Em Dry
</td></tr></tbody></table>
<h3><a name="1284">1284 &nbsp; The Modern Jazz Quartet Plays One Never Knows (No Sun In Venice)</a></h3>
Milt Jackson (vibraphone) John Lewis (piano) Percy Heath (bass) Connie Kay (drums)
<div class="date">NYC, April 4, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2500</td><td>Venice
</td></tr></tbody></table>
same personnel
<div class="date">"Music Inn", Lenox, MA, August 24, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2715</td><td>The Golden Striker
</td></tr><tr><td>2716</td><td>Cortege
</td></tr><tr><td>2717</td><td>One Never Knows
</td></tr><tr><td>2718</td><td>Three Windows
</td></tr><tr><td>2719</td><td>The Rose Truc
</td></tr></tbody></table>
** also issued on Atlantic SD 1284.
<h3><a name="1285">1285 &nbsp; Bobby Short - Sing Me A Swing Song</a></h3>
Bobby Short (piano, vocals) Ismael Ugarte (bass) Ramon "Sonny" Rivera (drums)
<div class="date">NYC, July 12, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2660</td><td>Montevideo
</td></tr><tr><td>2663</td><td>How Can You Forget
</td></tr></tbody></table>
Bernie Glow, Lou Oles, Nick Travis (trumpet) Warren Covington, Urbie Green (trombone) Romeo Penque (flute, alto saxophone, clarinet) Danny Bank (baritone saxophone) Bobby Short (piano, vocals) Barry Galbraith (guitar) Arnold Fishkin (bass) Jimmy Crawford (drums)
<div class="date">NYC, July 22, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2677</td><td>Don't Let It Get You Down
</td></tr><tr><td>2678</td><td>For No Rhyme And Reason
</td></tr><tr><td>2679</td><td>Some Fine Day
</td></tr><tr><td>2680</td><td>It's Bad For Me
</td></tr></tbody></table>
Don Elliott (trumpet, mellophone, trombone, vibraphone) Bobby Short (piano, vocals) Barry Galbraith (guitar) Pat Merola (bass) Ted Sommer (drums)
<div class="date">NYC, December 10, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2861</td><td>Lydia
</td></tr><tr><td>2862</td><td>I'm Checkin' Out, Go'om Bye
</td></tr><tr><td>2863</td><td>Rocks In My Bed
</td></tr><tr><td>2864</td><td>I Got What It Takes
</td></tr></tbody></table>
Bernie Glow, Lou Oles, Joe Wilder (trumpet) Phil Giacobbe, Jack Satterfield (trombone) Sol Schlinger (baritone saxophone, bass clarinet) Bobby Short (piano, vocals) Barry Galbraith (guitar) Clyde Lombardi (bass) Ted Sommer (drums)
<div class="date">NYC, December 18, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2769</td><td>Ace In The Hole
</td></tr><tr><td>2770</td><td>From Now On
</td></tr><tr><td>2771</td><td>Ebony Rhapsody
</td></tr><tr><td>2772</td><td>Wake Up, Chillun, Wake Up
</td></tr></tbody></table>
<h3><a name="1286">1286 &nbsp; A Jazz Date With Chris Connor</a></h3>
Joe Wilder (trumpet) Al Cohn (tenor saxophone) Eddie Costa (vibraphone) Ralph Sharon (piano, arranger) Oscar Pettiford (bass) Osie Johnson (drums) Chris Connor (vocals)
<div class="date">NYC, December 16, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2204</td><td>Poor Little Rich Girl
</td></tr><tr><td>2205</td><td>Everything I've Got
</td></tr><tr><td>2206</td><td>All I Need Is You
</td></tr><tr><td>2207</td><td>It Only Happens When I Dance With You
</td></tr></tbody></table>
Sam Most (flute) Joe Puma (guitar) replaces Wilder, Cohn
<div class="date">NYC, December 17, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2243</td><td>Lonely Town
</td></tr><tr><td>2244</td><td>Fancy Free
</td></tr><tr><td>2245</td><td>Moon Ray
</td></tr><tr><td>2246</td><td>Driftwood
</td></tr></tbody></table>
Al Cohn, Lucky Thompson (tenor saxophone) Eddie Costa (vibraphone) Ralph Sharon (piano, arranger) Oscar Pettiford (bass) Osie Johnson (drums) Ramon "Mongo" Santamaria (congas) Chino Pozo (bongos) Chris Connor (vocals)
<div class="date">NYC, December 19, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">2278</td><td>My Shining Hour
</td></tr><tr><td>2279</td><td>Just Squeeze Me
</td></tr><tr><td>2280</td><td>I'm Shooting High
</td></tr><tr><td>2281</td><td>It's A Most Unusual Day
</td></tr></tbody></table>
<h3><a name="1287">1287 &nbsp; John Lewis Presents Jazz Piano International</a></h3>
Rene Urtreger (piano) Paul Rovere (bass) Al Levitt (drums) John Lewis (supervisor)
<div class="date">Paris, France, April 20, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">4433</td><td>Fontainebleau (Fontaine-Blow)
</td></tr><tr><td>4434</td><td>Jumpin' At The Woodside
</td></tr><tr><td>4435</td><td>What's New
</td></tr><tr><td>4436</td><td>Monsieur De...
</td></tr></tbody></table>
Derek Smith (piano) Percy Heath (bass) Connie Kay (drums) John Lewis (supervisor)
<div class="date">NYC, June 12, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2598</td><td>Gone With The Wind
</td></tr><tr><td>2600</td><td>Chelsea Bridge
</td></tr><tr><td>2601</td><td>Thirty-Six Days
</td></tr></tbody></table>
Dick Katz (piano) Ralph Pena (bass) Connie Kay (drums) John Lewis (supervisor)
<div class="date">NYC, August 1, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2696</td><td>A Foggy Day
</td></tr><tr><td>2697</td><td>Don't Explain
</td></tr><tr><td>2698</td><td>Jeff And Jamie
</td></tr><tr><td>2699</td><td>There Will Never Be Another You
</td></tr></tbody></table>
<h3><a name="1288">1288 &nbsp; Wilbur DeParis Plays Cole Porter</a></h3>
Sidney DeParis (trumpet) Doc Cheatham (trumpet -1/4,7) Wilbur DeParis (trombone) Omer Simeon (clarinet) Sonny White (piano) Lee Blair (banjo) Benny Moten (bass) Wilbert Kirk (drums, harmonica)
<div class="date">NYC, February 25, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">1. 2616</td><td>Easy To Love
</td></tr><tr><td>2. 2618</td><td>I've Got You Under My Skin
</td></tr><tr><td>3. 2619</td><td>I Get A Kick Out Of You
</td></tr><tr><td>4. 2620</td><td>Anything Goes
</td></tr><tr><td>5. 2621</td><td>Love For Sale
</td></tr><tr><td>6. 2622</td><td>Wunderbar
</td></tr><tr><td>7. 2623</td><td>It's All Right With Me
</td></tr></tbody></table>
Sidney DeParis (trumpet) Wilbur DeParis (trombone) Omer Simeon (clarinet) Sonny White (piano) Lee Blair (banjo) Hayes Alvis (bass) Wilbert Kirk (drums)
<div class="date">NYC, May 26, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3071</td><td>Begin The Beguine
</td></tr><tr><td>3072</td><td>You Do Something To Me
</td></tr><tr><td>3073</td><td>It's All Right With Me
</td></tr></tbody></table>
<h3><a name="1289">1289 &nbsp; Ray Charles At Newport</a></h3>
Marcus Belgrave, Lee Harper (trumpet) David Newman (tenor, alto saxophone) Hank Crawford (baritone saxophone) Ray Charles (piano, alto saxophone, vocals) Edgar Willis (bass) Richie Goldberg (drums) Marjorie Hendricks (vocals) The Raelets (vocal group)
<div class="date">"Newport Jazz Festival", Newport, RI, July 5, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3121</td><td>(Spirit Feel) Hot Rod
</td></tr><tr><td>3122</td><td>Blues Waltz
</td></tr><tr><td>3123</td><td>In A Little Spanish Town
</td></tr><tr><td>3124</td><td>Sherry
</td></tr><tr><td>3125</td><td>The Right Time
</td></tr><tr><td>3126</td><td>A Fool For You
</td></tr><tr><td>3127</td><td>I Got A Woman
</td></tr><tr><td>3128</td><td>Talkin' 'Bout You
</td></tr></tbody></table>
** also issued on Atlantic SD 1289.
<h3><a name="1290">1290 &nbsp; Chris Connor - Chris Craft</a></h3>
Bobby Jaspar (flute, tenor saxophone) Stan Free (piano) Mundell Lowe (guitar) Percy Heath (bass) Ed Shaughnessy (drums) Chris Connor (vocals)
<div class="date">NYC, March 13, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">2998</td><td>Here Lies Love
</td></tr><tr><td>2999</td><td>The Night We Called It A Day
</td></tr><tr><td>3000</td><td>Blow, Gabriel, Blow
</td></tr><tr><td>3001</td><td>Chinatown, My Chinatown
</td></tr></tbody></table>
Al Epstein (bass clarinet) Stan Free (piano) Mundell Lowe (guitar) George Duvivier (bass) Ed Shaughnessy (drums) Chris Connor (vocals)
<div class="date">NYC, April 8, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3032</td><td>Be My All
</td></tr><tr><td>3033</td><td>One Love Affair
</td></tr><tr><td>3034</td><td>Good For Nothin' (But Love)
</td></tr><tr><td>3035</td><td>On The First Warm Day
</td></tr></tbody></table>
omit Epstein, Free
<div class="date">NYC, May 23, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3067</td><td>Be A Clown
</td></tr><tr><td>3068</td><td>Moonlight In Vermont
</td></tr><tr><td>3069</td><td>Lover Man
</td></tr><tr><td>3070</td><td>Johnny One Note
</td></tr></tbody></table>
<h3><a name="1291">1291 &nbsp; Warne Marsh</a></h3>
Warne Marsh (tenor saxophone) Ronnie Ball (piano) Paul Chambers (bass) Philly Joe Jones (drums)
<div class="date">NYC, December 12, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2871</td><td>Too Close For Comfort
</td></tr><tr><td>2872</td><td>It's All Right With Me
</td></tr></tbody></table>
Warne Marsh (tenor saxophone) Paul Chambers (bass) Paul Motian (drums)
<div class="date">NYC, January 16, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">2908</td><td>Yardbird Suite
</td></tr><tr><td>2909</td><td>My Melancholy Baby
</td></tr><tr><td>2910</td><td>Excerpt
</td></tr><tr><td>2911</td><td>Just Squeeze Me
</td></tr></tbody></table>
** also issued on Atlantic SD 1291.
<h3><a name="1292">1292 &nbsp; Here Is Chris Barber</a></h3>
Pat Halcox (cornet) Chris Barber (trombone) Monty Sunshine (clarinet) Lonnie Donegan (banjo) Jim Bray (bass) Ron Bowden (drums)
<div class="date">London, England, January 13, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">3324</td><td>Diga Diga Doo
</td></tr></tbody></table>
same personnel
<div class="date">London, England, March 3, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">3318</td><td>You Don't Understand
</td></tr></tbody></table>
same personnel
<div class="date">London, England, March 8, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">3317</td><td>Papa De-Da-Da
</td></tr><tr><td>3321</td><td>Everybody Loves My Baby
</td></tr></tbody></table>
same personnel
<div class="date">London, England, March 9, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">3319</td><td>Tishomingo Blues
</td></tr></tbody></table>
add Ben Cohen (cornet)
<div class="date">London, England, March 18, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">3329</td><td>Tuxedo Tag
</td></tr></tbody></table>
Pat Halcox (cornet) Chris Barber (trombone) Monty Sunshine (clarinet) Lonnie Donegan (banjo) Mickey Ashman (bass) Ron Bowden (drums)
<div class="date">London, England, September 16, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">3326</td><td>Doin' The Crazy Walk
</td></tr></tbody></table>
add Ottilie Patterson (vocals)
<div class="date">London, England, September 25, 1955</div>
<table width="100%">
<tbody><tr><td width="15%">3327</td><td>Magnolia's Wedding Day
</td></tr></tbody></table>
Monty Sunshine (clarinet) Lonnie Donegan (banjo) Mickey Ashman (bass) Ron Bowden (drums)
<div class="date">London, England, March 26, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">3322</td><td>Hush-A-Bye
</td></tr></tbody></table>
Pat Halcox (cornet) Chris Barber (trombone) Monty Sunshine (clarinet) Eddie Smith (banjo) Dick Smith (bass) Ron Bowden (drums)
<div class="date">London, England, December 15, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">3323</td><td>Willie The Weeper
</td></tr></tbody></table>
Pat Halcox (cornet) Chris Barber (trombone) Monty Sunshine (clarinet) Eddie Smith (banjo) Dick Smith (bass) Graham Burbidge (drums) Ottilie Patterson (vocals)
<div class="date">London, England, January 23, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3320</td><td>Trombone Cholly
</td></tr></tbody></table>
Monty Sunshine (clarinet) Eddie Smith (banjo) Dick Smith (bass) Graham Burbidge (drums)
<div class="date">"Town Hall", Birmingham, England, January 31, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3328</td><td>Bill Bailey
</td></tr></tbody></table>
<h3><a name="1293">1293 &nbsp; George Byron Sings New And Rediscovered Jerome Kern Songs</a></h3>
Andre Previn (piano, arranger, conductor) George Byron (vocals)
<div class="date">Los Angeles, CA, November 9, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">4466</td><td>The Touch Of Your Hand
</td></tr><tr><td>4467</td><td>Nice To Be Near You
</td></tr><tr><td>4468</td><td>Introduce Me
</td></tr><tr><td>4469</td><td>April Fooled Me
</td></tr></tbody></table>
same personnel
<div class="date">Los Angeles, CA, November 30, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">4470</td><td>Let's Begin
</td></tr><tr><td>4471</td><td>The Siren's Song
</td></tr><tr><td>4472</td><td>How'd You Like To Spoon With Me
</td></tr><tr><td>4473</td><td>You Couldn't Be Cuter
</td></tr><tr><td>4474</td><td>Two Hearts Together
</td></tr></tbody></table>
same personnel
<div class="date">Los Angeles, CA, April 29, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">4475</td><td>Long Ago And Far Away
</td></tr><tr><td>4476</td><td>Poor Pierrot
</td></tr><tr><td>4477</td><td>The Folks Who Live On The Hill
</td></tr></tbody></table>
** also issued on Atlantic SD 1293.
<h3><a name="1294">1294 &nbsp; Milt Jackson - Bags And Flutes</a></h3>
Bobby Jaspar (flute) Milt Jackson (vibraphone) Tommy Flanagan (piano) Kenny Burrell (guitar) Percy Heath (bass) Art Taylor (drums)
<div class="date">NYC, May 21, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2550</td><td>Bags' New Groove
</td></tr><tr><td>2551</td><td>Connie's Blues
</td></tr></tbody></table>
Frank Wess (flute) Milt Jackson (vibraphone) Hank Jones (piano) Kenny Burrell (guitar) Percy Heath (bass) Art Taylor (drums)
<div class="date">NYC, June 10, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2582</td><td>Midget Rod
</td></tr><tr><td>2583</td><td>I'm Afraid The Masquerade Is Over
</td></tr><tr><td>2584</td><td>Sweet And Lovely
</td></tr></tbody></table>
same personnel
<div class="date">NYC, June 17, 1957</div>
<table width="100%">
<tbody><tr><td width="15%">2603</td><td>Sandy
</td></tr><tr><td>2604</td><td>Ghana
</td></tr></tbody></table>
** also issued on Atlantic SD 1294.
<h3><a name="1295">1295 &nbsp; Jimmy Giuffre - The Four Brothers Sound</a></h3>
Jimmy Giuffre (four overdubbed tenor saxophone)
<div class="date">Atlantic Studios, NYC, June 23, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3081</td><td>Come Rain Or Come Shine
</td></tr></tbody></table>
same personnel
<div class="date">Atlantic Studios, NYC, June 25, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3083</td><td>Ode To Switzerland
</td></tr></tbody></table>
Jimmy Giuffre (four overdubbed tenor saxophone) Bob Brookmeyer (piano) Jim Hall (guitar)
<div class="date">Lenox, MA, September 1, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3148</td><td>I Got The Right To Sing The Blues
</td></tr><tr><td>3149</td><td>Space
</td></tr><tr><td>3150</td><td>Cabin In The Sky
</td></tr><tr><td>3151</td><td>Memphis In June
</td></tr><tr><td>3152</td><td>Four Brothers
</td></tr><tr><td>3153</td><td>Old Folks
</td></tr><tr><td>3154</td><td>Blues In The Barn
</td></tr></tbody></table>
** also issued on Atlantic SD 1295.<br>
** part of Mosaic MQ10-176, MD6-176.
<h3><a name="1296">1296 &nbsp; Various Artists - Voodoo Drums In Hi-Fi</a></h3>
unknown artists
<div class="date">April, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">4497</td><td>Contradanse: Avant Simple With Flute
</td></tr><tr><td>4498</td><td>Ti-Roro Drum Solo I
</td></tr><tr><td>4499</td><td>Ti-Joe Carabien
</td></tr><tr><td>4500</td><td>Meringue With Flute
</td></tr><tr><td>4501</td><td>Nan Point La Vie Encore Oh!
</td></tr><tr><td>4502</td><td>Laissez Yo Di
</td></tr><tr><td>4503</td><td>Rara Riffs
</td></tr><tr><td>4504</td><td>Contradanse: Avant Simple With Accordion
</td></tr><tr><td>4505</td><td>Annonce Oh Zange Nan Dio
</td></tr><tr><td>4506</td><td>Contradanse: Avant Simple And Meringue With Flute
</td></tr><tr><td>4507</td><td>Misere Pa Douce!
</td></tr><tr><td>4508</td><td>Ti-Roro Drum Solo II
</td></tr></tbody></table>
<h3><a name="1297">1297 &nbsp; Young Tuxedo Brass Band - Jazz Begins</a></h3>
Andrew Anderson, John Brunious, Albert Walters (trumpet) Jim Robinson or Eddie Pierson, Clement Tervalon (trombone) John Casimir (E flat clarinet, leader) Herman Sherman (alto saxophone) Andrew Morgan (tenor saxophone) Wilbert Tillman (sousaphone) Paul Barbarin (snare drum) Emile Knox (bass drum)
<div class="date">New Orleans, LA, November 1, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">5335</td><td>John Casimir's Whoopin' Blues
</td></tr><tr><td>5336</td><td>Eternal Peace
</td></tr><tr><td>5337</td><td>Lead Me Saviour
</td></tr><tr><td>5338</td><td>Medley: Free As A Bird / Nearer My God To Thee / Pleyel's Hymn
</td></tr><tr><td>5340</td><td>Joe Avery's Piece
</td></tr><tr><td>5341</td><td>Panama
</td></tr><tr><td>5342</td><td>Just A Closer Walk With Thee
</td></tr><tr><td>5344</td><td>Bourbon Street Parade
</td></tr><tr><td>5345</td><td>It Feels So Good
</td></tr></tbody></table>
same personnel
<div class="date">New Orleans, LA, November 2, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">5347</td><td>Lord, Lord, Lord, You've Sure Been Good To Me
</td></tr><tr><td>5350</td><td>Just A Little While To Stay Here
</td></tr></tbody></table>
** also issued on Atlantic SD 1297.

<h3><a name="1298">1298 &nbsp; Various Artists - Historic Jazz Concert At Music Inn</a></h3>
Jimmy Giuffre, Pee Wee Russell (clarinet) George Wein (piano) Oscar Pettiford (bass) Connie Kay (drums)
<div class="date">"Music Inn", Lenox, MA, August 30, 1956</div>
<table width="100%">
<tbody><tr><td width="15%">3356</td><td>Blues In E-Flat
</td></tr></tbody></table>
Rex Stewart (trumpet) Jimmy Giuffre (tenor saxophone) George Wein (piano) Oscar Pettiford (bass) Connie Kay (drums)
<div class="date"></div>
<table width="100%">
<tbody><tr><td width="15%">3357</td><td>In A Mellotone
</td></tr></tbody></table>
Jimmy Giuffre (clarinet) Teddy Charles (vibraharp) Percy Heath (bass) Connie Kay (drums)
<div class="date"></div>
<table width="100%">
<tbody><tr><td width="15%">3358</td><td>The Quiet Time
</td></tr></tbody></table>
Herbie Mann (flute) Dick Katz (piano) Oscar Pettiford (cello) Ray Brown (bass) Connie Kay (drums)
<div class="date"></div>
<table width="100%">
<tbody><tr><td width="15%">3359</td><td>Body And Soul
</td></tr></tbody></table>

<h3><a name="1299">1299 &nbsp; The Modern Jazz Quartet At Music Inn, Vol. 2 - Guest Artist: Sonny Rollins</a></h3>
Milt Jackson (vibraphone) John Lewis (piano) Percy Heath (bass) Connie Kay (drums)
<div class="date">"Music Inn", Lenox, MA, August 3, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3143</td><td>Yardbird Suite
</td></tr><tr><td>3145</td><td>Festival Sketch
</td></tr><tr><td>3146</td><td>Midsommer
</td></tr><tr><td>3147</td><td>Medley: Stardust / I Can't Get Started / Lover Man
</td></tr></tbody></table>
add with guest artist: Sonny Rollins (tenor saxophone)
<div class="date">"Music Inn", Lenox, MA, August 31, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3937</td><td>Bags' Groove
</td></tr><tr><td>3938</td><td>Night In Tunisia
</td></tr></tbody></table>
** also issued on Atlantic SD 1299.


<h3><a name="1300">1300 &nbsp; Wilbur DeParis Plays Something Old, New, Gay, Blue</a></h3>
Doc Cheatham, Sidney DeParis (trumpet) Wilbur DeParis (trombone) Omer Simeon (clarinet) Sonny White (piano) Lee Blair (banjo) Hayes Alvis (bass) Wilbert Kirk (drums)
<div class="date">NYC, May 26, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3074</td><td>Bouquets
</td></tr><tr><td>3075</td><td>Beale Street Blues
</td></tr></tbody></table>
Sidney DeParis (trumpet) Wilbur DeParis (trombone) Omer Simeon (clarinet, soprano saxophone) Sonny White (piano) Lee Blair (banjo) Hayes Alvis (bass) Wilbert Kirk (drums, harmonica)
<div class="date">NYC, June 30, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3087</td><td>Band Jolie (Banjolie)
</td></tr><tr><td>3088</td><td>Madeira
</td></tr><tr><td>3089</td><td>Panama Rag
</td></tr><tr><td>3090</td><td>High Society
</td></tr><tr><td>3092</td><td>Muskrat Ramble
</td></tr></tbody></table>
Doc Cheatham, Sidney DeParis (trumpet) Wilbur DeParis (trombone) Omer Simeon (clarinet) Sonny White (piano) Lee Blair (banjo) Hayes Alvis (bass) Wilbert Kirk (drums)
<div class="date">NYC, December 15, 1958</div>
<table width="100%">
<tbody><tr><td width="15%">3238</td><td>Colonel Bogey's March
</td></tr></tbody></table>
** also issued on Atlantic SD 1300.
<!-- id="catalog-data" -->
"""

text="""<h3>1</h3>
<h3>Text<Subform/></h3>
<h3></h3>
Text
<div></div>"""


#################################################################################################################################################
###Regular Expression Approach to Parse 3 Function###############################################################################################
#################################################################################################################################################

##################################
# Define and Compile Expressions #
##################################

'''
Expression Name:	Purpose:
p1			Grabs record series blocks
q1			Grabs record series block names
p2			Takes record type block, splits into album blocks
p3			Takes album block, extracts title

note: For the following RE's we assume that existence of one instance of a feature implies existence of the other features, so they all share 		common indices when extracted. That is if these expressions return lists of length greaterthan 1 item, then we safely assume all the 
	n-th items the different lists are assosciated to the same block of information.

p4			Takes album block, extracts personnel lists
p5			Takes album block, extracts location date strings
p6			Takes album block, extracts song lists

note: The following RE's are for the cleanup functions

s1			Cleans the songlist
s2			Detects the date in dateLoc
s3			Detects the loc  "	"
s4			Detects player, instrument tuples in personnel
s5			Used for removing those pesky \n signs
'''

p1 = re.compile(r'<h2>.*?(?=<h2>|$)', re.DOTALL) 
q1 = re.compile(r"(?<=<h2>).*?(?=</h2>)") 
p2 = re.compile(r'<h3>.*?(?=<h3>|$)', re.DOTALL) 
p3 = re.compile(r'(?<=nbsp; ).*(?=</a>)', re.DOTALL) 
p4 = re.compile(r'(?<=</h3>).*?(?=<div class="date">)|(?<=</table>).*?(?=<div class="date">)', re.DOTALL)
p5 = re.compile(r'(?<=<div class="date">).*?(?=</div>)', re.DOTALL) 
p6 = re.compile(r'(?<=<table width="100%">).*?(?=</table>)', re.DOTALL) 
s1 = re.compile(r"(?<=</td><td>).+?(?=\n</td>)",re.DOTALL)
s2 = re.compile(r"(?<=, )\w+? [0-9]+, [0-9]+")
s3 = re.compile(r".+?(?=, \w+? [0-9]+, [0-9]+)")
s4 = re.compile(r"(.+?)[(](.+?)[)]")
s5 = re.compile(r"\n")

############################
# Define Cleanup Functions #
############################

def songClean(songList):
	cleanList=[]
	for song in songList:
		entry=s1.findall(song)		
		cleanList.append(entry)
	return cleanList

def dateClean(dateLocList):
	'''
	Takes a list containing strings of the form '(place), (date)'
	and spits out solely the date strings.
	'''	
	dateList=[]
	for dateLoc in dateLocList:
		try:
			date = s2.findall(dateLoc)[0]
		except IndexError:		
			date = ""			
		dateList.append(date)
	for i in xrange(len(dateList)):
		if dateList[i]=="":
			if i==0:
				dateList[i]="NA"
			else:
				dateList[i]=dateList[i-1]
	return dateList

def locClean(dateLocList):
	'''
	Takes a list containing strings of the form '(place), (date)'
	and spits out solely the place strings.	
	'''
	locList=[]
	for dateLoc in dateLocList:
		try:
			loc = s3.findall(dateLoc)[0]
		except IndexError:
			loc = ""
		locList.append(loc)
	for i in xrange(len(locList)):
		if locList[i]=="":
			if i==0:
				locList[i]="NA"
			else:
				locList[i]=locList[i-1]
	return locList

def personnelClean(personnelList):
	'''
	Cleans personnel list into a list of tuples for players and instruments.
	Note: Multiple players in front of an instrument are all assumed to play that instrument
	Note: We need functionality to account for directions such as 'omit this player', 'previous lineup', etc...
	'''
	out=[]
	for subList in personnelList:
		subList = s5.sub("",subList)
		subOut = s4.findall(subList)
		corrected = []
		for i in xrange(len(subOut)):
			try:
				if "," in subOut[i][0]:
					offender=subOut.pop(i)
					for name in offender[0].split(", "):
						corrected.append((name,offender[1]))
			except IndexError:
				pass
		subOut = subOut + corrected
		out.append(subOut)
	return out

#############
# Algorithm #
#############

#1. Split By Record Series:
recList = p1.findall(doc)
for rec in recList:
	#2. Grabs Series' Names
	recSeries = q1.search(rec).group()
	#3. Split HTML by album
	recList = p2.findall(rec)
	for album in recList:
		#4. Extract relevant info from album HTML chunks
		#	and clean output.
		out = Album()
		
		out['recSeries'] = recSeries

		title=p3.findall(album)[0]
		out['title'] = title
		
		personnel = p4.findall(album)
		personnel = personnelClean(personnel)
		out['personnelList'] = personnel

		dateLoc = p5.findall(album)
		dateList = dateClean(dateLoc)
		locList = locClean(dateLoc)
		out['dateList'] = dateList
		out['locList'] = locList

		songs = p6.findall(album)
		songs = songClean(songs)
		out['songList'] = songs


##############################################
# Print Return Fields for Debugging Purposes #
##############################################
		
print "\nRecord Series:\n"
print recSeries
print "\nTitle:\n"
print title
print "\nPersonnel List:\n"
print personnel
print "\nDates and Locations:\n"
print dateList
print locList
print "\nSongs:\n"
print songs
	


