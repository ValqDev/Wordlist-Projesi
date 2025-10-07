import random
import datetime
from typing import Optional, List, Dict, Any

Baslangic = input("""



                                                                        
                                                                        
                                                                        
                               #***##**##                               
                         ######################                         
                    ######**+-..:--=--::.:=*#######                     
                 -+**#*+-.-                  :.-*#*#++:                 
                ++=*+::                          :-*=++=                
               ###=#.:                            .=*=#                 
           --#####+*-     :..:--        -::..-     =+*####+:            
          :*#=.  =    :..-:-....-      ....:::-..        .*#=-          
         :###..:      :=  :......:: -.-......:  -       ..-##=:         
        -+###....:        -......:    ......:+        ....=###=#        
       *=##:*+......         ......-......:        :.....:#-*#*+        
       #+##..:#+.......       ....-:::...=      ........*+..=##+#       
      ##=##.....-*:....      +:....=:...:-      .....-+.....*#*+##      
     ##**###-..........:     -............=     ...........+###*##      
     #####..:+##+=-.....:  :.....::::::.....=  .....:=+*#*=:.+####*     
     ##+##*................=-=-+%%######=-=-:................##*###     
     ##-#####+=...:*.........+    +=+*####+........==...-+*####+###     
    ###-###:..:=#+...=.......   -.-########......:=..-**-:..+##+###     
     ##-*##=-:....:*:.:-.....   ..#####:-#+.....=..=*....:-=###=###     
     *#++###-..-#*...*:..::..=  :.+#######...-...+-..-#*:..*###=###     
     ###-###*+=:...:#..-..-...+###:.-=###-...=.=..-*....-+*###*-###     
     ###=*###:....=*..-+..*....=########-...-+..*...#:....+###-##*      
      ###-####-..#=...*:.=:=....:#####*...:.-=..+=...*+..+###*=##       
       ##*-#####*....=*..*..+#*...:*+...-##:.-=.:#....-######-##*       
        ##*=###+.....#-..#.*##---......=.*##=:*..+*.....####:##*        
         ###=####+=*#=.:.#+###:..=...::..=###=#...##+=*###*-##*         
          ###-####*.-*##:=*++##....:-...-#*+**:*##=.:####++###          
           ###+=#####=*+=:-**-#--+-..+--+*=*+::=+++#####:###            
             ###=+###+=###+::#:..#.+=.+..=*.=*###:####-*###             
               ###+-#####..-#...+.+..*+:..-#..-#####:*###               
                 ####-+#####...==:+..#.*...-#####-+###*                 
                    ####+=+##**#.:=..#.=#+###+=*###*                    
                       #####+-####*.:####*-+#####                       
                            #**+:#####*-***                             
                                  :*=:                                  
                                                                    
                                                                        
                                                                        
Eğer Programı Başlatmak İsterseniz Enter'a Basın...



""")

def synth_profile() -> Dict[str, Any]:
    """
    Kullanıcıdan alınan bilgileri parse edip profil sözlüğü döndürür.
    Boş bırakılabilir alanlar desteklenir.
    """
    first = input("İsim (boş bırakabilirsiniz): ").strip()
    last = input("Soyadı (boş bırakabilirsiniz): ").strip()
    birth_raw = input("Doğum tarihi (YYYY veya YYYY-MM-DD veya DD.MM.YYYY, boş bırakabilirsiniz): ").strip()

    birth_date: Optional[datetime.date] = None
    if birth_raw:
        for fmt in ("%Y-%m-%d", "%Y", "%d.%m.%Y", "%d/%m/%Y"):
            try:
                parsed = datetime.datetime.strptime(birth_raw, fmt)
                if fmt == "%Y":
                    birth_date = datetime.date(parsed.year, 1, 1)
                else:
                    birth_date = parsed.date()
                break
            except ValueError:
                continue
    if birth_date is None and birth_raw:
        print("Uyarı: Doğum tarihi okunamadı. Varsayılan boş tarih kullanılacak.")
        birth_date = None

    spouse = input("Eş adı (boş bırakabilirsiniz): ").strip() or None
    company = input("Çalıştığı Şirket (boş bırakabilirsiniz): ").strip()
    children_raw = input("Çocuk isimleri (virgülle ayrılmış, boş bırakabilirsiniz): ").strip()
    children = [c.strip() for c in children_raw.split(",") if c.strip()] if children_raw else []

    return {
        "first": first,
        "last": last,
        "birth": birth_date,
        "spouse": spouse,
        "company": company,
        "children": children
    }

def year_str(d: Optional[datetime.date]) -> str:
    return str(d.year) if d else ""

def birth_ddmm(d: Optional[datetime.date]) -> str:
    return f"{d.day:02d}{d.month:02d}" if d else ""

def generate_candidates(profile: Dict[str, Any], max_per_profile: int = 30000000000000000000000000000000000000) -> List[str]:
    f = profile.get("first", "")
    l = profile.get("last", "")
    birth = profile.get("birth")
    y = year_str(birth)
    ddmm = birth_ddmm(birth)

    company = profile.get("company", "")
    company_first = company.split()[0] if company else ""
    kids: List[str] = profile.get("children", []) or []
    spouse = profile.get("spouse") or ""

    candidates = set()

    base_patterns = [
        f"{f}{y}",
        f"{f}{y[-2:]}" if y else f"{f}",
        f"{f}{l}",
        f"{f}{l}{y[-2:]}" if y else f"{f}{l}",
        f"{f}{ddmm}" if ddmm else f"{f}",
        f"{f}{company_first}" if company_first else f"{f}",
        f"{f}123" if f else "",
        f"{f}!{y[-2:]}" if y else f"{f}!",
        f"{f}.{l}" if l else f"{f}",
        f"{f}_{y}" if y else f"{f}_",
    ]

    if spouse:
        base_patterns += [f"{f}{spouse}", f"{spouse}{y[-2:]}" if y else f"{spouse}"]

    for k in kids:
        base_patterns += [f"{f}{k}", f"{k}{y[-2:]}" if y else f"{k}"]

    counter = 0
    while len(candidates) < max_per_profile:
        for p in base_patterns:
            if not p:
                continue
            candidates.add(p)
            candidates.add(p.lower())
            candidates.add(p.capitalize())
            candidates.add(p + "!")
            candidates.add(p + "01")
            candidates.add(p + str(random.randint(100,999)))  

            counter += 1
            if len(candidates) >= max_per_profile:
                break
        if counter > max_per_profile * 2:
            break

    return list(sorted(candidates))[:max_per_profile]

def main(out_file: str = "lab_wordlist.txt", profiles: int = 10, per_profile: int = 25):
    with open(out_file, "w", encoding="utf-8") as f:
        for i in range(profiles):
            print(f"\n--- Profil {i+1}/{profiles} için bilgi giriniz ---")
            prof = synth_profile()
            cands = generate_candidates(prof, max_per_profile=per_profile)
            birth_iso = prof["birth"].isoformat() if isinstance(prof["birth"], datetime.date) else ""
            f.write(f"# PROFILE: {prof['first']} {prof['last']} | birth:{birth_iso} | company:{prof['company']}\n")
            for c in cands:
                f.write(c + "\n")
            f.write("\n")
    print(f"{out_file} oluşturuldu (sadece sentetik/veri örnekleri).")

if __name__ == "__main__":
    main(out_file="lab_wordlist.txt", profiles=1, per_profile=50000)
