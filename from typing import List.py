from typing import List, Optional

def build_roster(names: List[Optional[str]], extra: List[str] = None):
    if extra is None:
        extra = []
    

    filtered_names = [name for name in names if isinstance(name, str)]
    
    copy_names = filtered_names.copy()
    
    merged = copy_names + extra
    

    for i in range(len(merged)):
        merged[i] = merged[i].strip().title()
    
    return merged

def main():
    students = ["\t  анНА  ", "  ", "", None, "пЁТР"]
    extra = []
    
    if any(isinstance(item, str) for item in students):
        
        roster = build_roster(students, extra)
        
        print("Исходный students:", set(students))
        print("Результат roster:", set(roster))
        print("Длина исходного:", len(students))
        print("Длина результата:", len(roster))

if __name__ == "__main__":
    main()