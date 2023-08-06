
ones ={ 
    0: "", 
    1:" یک ",
    2:" دو ",
    3:" سه ",
    4:" چهار ",
    5:" پنج ",
    6:" شش ",
    7:" هفت ",
    8:" هشت ",
    9:" نه ",
    10:" ده ",
    11:" یازده ",
    12:" دوازده ",
    13:" سیزده ",
    14:" چهارده ",
    15:" پانزده ",
    16:" شانزده ",
    17:" هفده ",
    18:" هجده ",
    19:" نوزده "
    }
tens = {
    2:" بیست ",
    3:" سی ",
    4:" چهل ",
    5:" پنجاه ",
    6:" شصت ",
    7:" هفتاد ",
    8:" هشتاد ",
    9:" نود "}

hund={
        1:" صد ",
        2:" دويست ",
        3:" سيصد ",
        4:" چهارصد ",
        5:" پانصد ",
        6:" ششصد ",
        7:" هفتصد ",
        8:" هشتصد ",
        9:" نهصد "
        }    


illions = {
    1: 'هزار', 
    2: 'میلیون', 
    3: 'بيليون',
    4: 'تريليون'
    ,5: 'کوادريليون',
    6: 'کوئینتیلیون'
    ,7: 'سیکستیلیون'
    ,8: 'سپتیلیون'
    ,9: 'اکتیلیون',
    10: 'نونیلیون'
    ,11: 'دسیلیون'
    ,12:"آن دسیلیون"
    ,13:"دو دسیلیون"
    ,14:"تری دسیلیون"
    ,15:"کواتر دسیلیون"
    ,16:"کوئین دسیلیون"
    ,17:"سیکس دسیلیون"
    ,18:"سپتن دسیلیون"
    ,19:"اکتو دسیلیون"
    ,20:"نووم دسیلیون"
    ,21:"ویجینتیلیون"
    ,22:"آن ویجینتیلیون"
    ,23:" دو ویجینتیلیون"
    ,24:"تری ویجینتیلیون"
    ,25:"کواتر ویجینتیلیون"
    ,26:"کوئین ویجینتیلیون"
    ,27:"سیکس ویجینتیلیون"
    ,28:"سپتن ویجینتیلیون "
    ,29:"اکتو ویجینتیلیون"
    ,30:"نووم ویجینتیلیون"
    ,31:"تری جینتیلیون"
    ,32:"آن تری جینتیلیون"
    ,33:"دو تری جینتیلیون"}
        





def say_number(i):

    if i < 0:
        return ('منفی'+ say_number(-i))
    #if i == 0:
    #   return 'صفر'

    if i < 20:
        return ones[i]

    if i < 100:
        if i%10!=0:
            return (tens[i // 10]+"و"+ones[i % 10])
        else :
            return tens[i // 10]

    if i < 1000:
        if i%100!=0:
            return  hund[i // 100] + "و"+say_number(int(i % 100))

        else:
            return  hund[i // 100] +say_number(int(i % 100)) 
    
    
    for illions_number, illions_name in illions.items():
        if i < 1000**(illions_number + 1):
            break
    return _divide(i, 1000**illions_number, illions_name)



def _divide(dividend, divisor, magnitude):

    if dividend % divisor!=0:
    
        return _join(
            say_number(dividend // divisor),
            magnitude,"و",
            say_number(dividend % divisor),
        )

    else:
        return _join(
            say_number(dividend // divisor),
            magnitude,
            say_number(dividend % divisor),
        )

    
def _join(*args):
    return ' '.join(filter(bool, args))    
        



if __name__ == '__main__':
    print(say_number(
        
    ))
    
