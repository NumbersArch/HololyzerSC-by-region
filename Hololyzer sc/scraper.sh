#!/bin/bash  
#bash scraper.sh "DlJcWdiMREQ"
videoidnumber=11
prestring="https://hololyzer.net/youtube/archive/superchat/"
plfile="list.txt"
htmlfolder="Misc"
sleeptime=1

playlist=false
while getopts "p" arg; do
  case $arg in
	p)
		playlist=true   
		;;
	*)
		echo "Incorrect options"
		exit
		;;
  esac
done

proceed=true
if [ "$#" -lt 1 ]; then
    echo "Input Video ID"
    proceed=false  
fi
if [ "$#" -gt 1 ]; then
    echo "Too many parameters"
    proceed=false  
fi

if [ "$proceed" = false ]; then
	exit
else
	echo "Downloading files..."	
fi

if [ "$playlist" = false ]; then

	videoID="$1"
	if [ ${#videoID} -ne 11 ]; then
		echo "Video ID is wrong"
	else
	
		mkdir -p "raw/html/$htmlfolder"
		outputname="raw/html/$htmlfolder/$videoID.html"
		if [ ! -f "$outputname"  ]; then
			pagename="$prestring$videoID.html"
			if curl --head -s -o /dev/null --fail $pagename ;
			 then
				wget --random-wait -w 3 -O "$outputname" "$pagename"
			 else
			 	 echo "The page for $videoID does not exist."
			fi
		

		fi
			python3 py/process.py "$videoID" "$htmlfolder"

	fi

else
	
	listarray=(); counter=0
	while IFS= read -r line; do
	    l="$(echo "$line" | xargs)"
	    
	    if [[ $l == "~ "* ]]; then
	    	l="$(echo "${l#\~}" | xargs)"
		htmlfolder="$l"
		counter=$((counter+1))
		if [ "$counter" -eq 2 ]; then
			echo "Too many title designations"
			exit
		fi
	    	continue
	    fi
	    
	    if [[ "$l" == "" ]]; then
	    	continue
	    fi
	    if [[ $l == *"/playlist?list=PL"* ]]; then
	    	
	    	readarray -d "?" -t array <<< "$l" 
	    	lname=""
		for word in "${array[@]}"; 
		do 
		 lname="$word" 
		done
		
		if [ ${#lname} -ne 40 ]; then
			echo "Playlist $lname is wrong"
			exit
		else
		
		listvals="$(python3 py/getplaylist.py "$lname")"
		listarray+=($listvals)
		fi
		
	    else
	    
		    if [ ${#l} -ne 11 ]; then
		    	echo "VideoID $l is wrong"
		    	exit
		    	else
		    	listarray+=($l)
		    fi
	    
	    fi
	    
	done < $plfile
	arraystring="$( IFS=$'\n'; echo "${listarray[*]}" )"
	IFS=$'\n' read -d '' -r -a fullarray <<<"$arraystring"
	
	pstring=""; parray=()
	for videoID in "${fullarray[@]}"; 
	do 
		pagename="$prestring$videoID.html"
		if curl --head -s -o /dev/null --fail $pagename ;
		 then
			pstring="$pstring~$videoID"
			parray+=($videoID)
		 else
		 	 echo "The page for $videoID does not exist."
		fi
	done
	pstring="$(echo "${pstring#\~}" | xargs)"
	
	mkdir -p "raw/html/$htmlfolder"
	for videoID in "${parray[@]}"; 
	do 
		outputname="raw/html/$htmlfolder/$videoID.html"
		if [ ! -f "$outputname"  ]; then
			wget --random-wait -w 3 -O "$outputname" "$pagename"

		fi
	done
	
	python3 py/process.py "$pstring" "$htmlfolder"
fi

