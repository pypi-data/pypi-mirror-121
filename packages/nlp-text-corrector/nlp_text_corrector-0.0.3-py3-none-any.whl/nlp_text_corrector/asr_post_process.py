ordinal_nos=["first","second","third","fifth","eighth","ninth","twelfth"]
ordinal_nos_dict = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}

starting_nos=["zero","one","two","three","four","five","six","seven","eight","nine","ten",
              "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]
starting_nos_dict=dict()
for i in range(len(starting_nos)):
    starting_nos_dict[starting_nos[i]]=i

tens=["twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]
tens_dict=dict()
for i in range(len(tens)):
    tens_dict[tens[i]]=(i+2)*10

higher_nos=["hundred","thousand","million"]
higher_nos_dict={"hundred":100, "thousand":1000, "million":1000000}

ordinal_suffix_dict = {'first':'st', 'second':'nd', 'third':'rd', 'fifth':'th', 'eighth':'th', 'ninth':'th', 'twelfth':'th'}
ordinal_endings = [('ieth', 'y'), ('th', '')]

times = ["am", "pm", "hours", "hour", "alarm"]
prefix_times = ["alarm", "alarms", "meeting"]
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]    
    
def _corrections(fstring):
    fstring = fstring.replace("1st name", "first name")
    fstring = fstring.replace("1st class", "first class")
    fstring = fstring.replace("1 way", "one way")
    fstring = fstring.replace("2 way", "two way")
    fstring = fstring.split()
    for i,word in enumerate(fstring):
        if word in months and (i+1)<len(fstring) and fstring[i+1].isdigit(): 
            if len(fstring[i+1])>=5:
                year = fstring[i+1][-4:]
                date = fstring[i+1][:-4]
                fstring[i+1] = date
                fstring.insert(i+2, year)
    fstring = " ".join(fstring)
    return fstring

def convert(text): 

    text=text.replace("."," . ")
    text=text.replace("?"," ? ")
    text=text.replace("!"," ! ")
    text = text.replace("-"," ")
    
    tokens=text.split()

    temp_number=0
    final_number=0

    point_flag=False
    ordinal_flag=False
    number_flag=False
    word_flag=False
    prev_word_number_flag=False
    url_flag = False
    
    ones_flag=False
    tens_flag=False
    
    prefix_times_flag=False

    final_string=""
    ordinal_suffix=""

    tokens.append("")

    for i in range(len(tokens)):
        word=tokens[i]
        for ending, replacement in ordinal_endings:
            if word.endswith(ending):
                parted_word = "%s%s" % (word[:-len(ending)], replacement)
                if (parted_word.lower() in starting_nos or parted_word.lower() in tens or parted_word.lower() in higher_nos_dict):
                    word = parted_word
                    ordinal_suffix="th"
                    ordinal_flag=True
        if (word.lower() in ordinal_nos or word.lower() in starting_nos or word.lower() in tens or word.lower() in higher_nos_dict) and point_flag==False:             
            number_flag=True
            word_flag=False
            if word.lower() in ordinal_nos:
                if ones_flag:
                    final_number=final_number+temp_number
                    if not prev_word_number_flag:
                        final_string+=" "
                    final_string+=str(final_number)
                    final_number=0
                    temp_number=0
                    ones_flag=False
                    tens_flag=False
                    prev_word_number_flag=True
                temp_number=temp_number+ordinal_nos_dict[word.lower()]
                ordinal_suffix=ordinal_suffix_dict[word.lower()]
                ordinal_flag=True
            if word.lower() in starting_nos:
                if ones_flag or (tens_flag and starting_nos.index(word.lower())>=10):
                    final_number=final_number+temp_number
                    if not prev_word_number_flag:
                        final_string+=" "
                    final_string+=str(final_number)
                    final_number=0
                    temp_number=0
                    ones_flag=False
                    tens_flag=False
                    prev_word_number_flag=True
                temp_number=temp_number+starting_nos_dict[word.lower()]
                ones_flag=True
            elif word.lower() in tens:
                if ones_flag or tens_flag:
                    final_number=final_number+temp_number
                    if not prev_word_number_flag:
                        final_string+=" "
                    final_string+=str(final_number)
                    final_number=0
                    temp_number=0
                    ones_flag=False
                    tens_flag=False
                    prev_word_number_flag=True
                temp_number=temp_number+tens_dict[word.lower()]
                tens_flag=True

            elif word.lower()=="hundred":
                if temp_number==0:
                    temp_number=1
                temp_number=temp_number*100
                ones_flag=False
                tens_flag=False

            elif word.lower() in ["thousand","million"]:
                if temp_number==0:
                    temp_number=1
                final_number=final_number+temp_number*higher_nos_dict[word.lower()]
                temp_number=0
                ones_flag=False
                tens_flag=False
                
        elif word.lower() in starting_nos and point_flag==True:
            final_string+=str(starting_nos_dict[word.lower()])
            prev_word_number_flag=True

        elif (word=="and" and (tokens[i+1] in starting_nos or tokens[i+1] in tens or tokens[i+1] in higher_nos )):
            if ones_flag or tens_flag:
                final_number=final_number+temp_number
                if not prev_word_number_flag:
                    final_string+=" "
                final_string+=str(final_number)+" and"
                final_number=0
                temp_number=0
                ones_flag=False
                tens_flag=False
                prev_word_number_flag=False
            if word_flag:
                final_string+=" and"
                prev_word_number_flag=False
            continue

        elif (word.lower()=="point" and (tokens[i+1] in starting_nos or tokens[i+1] in tens or tokens[i+1] in higher_nos)):
            final_number=final_number+temp_number 
            point_flag=True
            number_flag=False
            if not prev_word_number_flag:
                final_string+=" "
            final_string+=str(final_number)+"."
            ones_flag=False
            tens_flag=False
            prev_word_number_flag=True
            continue
        
        else:
            if word.lower() in prefix_times:
                prefix_times_flag=True
            point_flag=False
            word_flag=True
            if number_flag==True:
                final_number=final_number+temp_number
                if (word.lower() in times or prefix_times_flag) and prev_word_number_flag:
                    final_string+=":"
                    if final_number<10:
                        final_string+="0"
                elif not prev_word_number_flag or word.lower() in months:
                    final_string+=" "
                if word!="." and word!="?" and word!="!" and word!="dot" and (word!="at" or (i+2>=len(tokens) or (i+2<len(tokens) and tokens[i+2]!="dot"))):
                    final_string+=str(final_number)+" "+word
                elif word=="dot":
                    final_string+=str(final_number)+"."
                    url_flag=True
                elif word=="at":
                    final_string+=str(final_number)+"@"
                    url_flag=True
                else:
                    final_string+=str(final_number)+word
                number_flag=False
                ones_flag=False
                tens_flag=False
            else:
                if url_flag:
                    final_string+=word
                    url_flag=False
                elif word!="." and word!="?" and word!="!" and word!="dot" and (word!="at" or (i+2>=len(tokens) or (i+2<len(tokens) and tokens[i+2]!="dot"))): 
                    final_string+=" "+word
                elif word=="dot":
                    final_string+="."
                    url_flag=True
                elif word=="at":
                    final_string+="@"
                    url_flag=True
                else: 
                    final_string+=word
            final_number=0
            temp_number=0
            prev_word_number_flag=False
        if ordinal_flag:
            final_number=final_number+temp_number
            if not prev_word_number_flag or tokens[i+1].lower() in months:
                final_string+=" "
            final_string+=str(final_number)+str(ordinal_suffix)
            final_number=0
            temp_number=0
            number_flag=False
            ordinal_flag=False
            ones_flag=False
            tens_flag=False
            prev_word_number_flag=False

    final_string=final_string[1:-1]
    final_string=_corrections(final_string)
    return(final_string)