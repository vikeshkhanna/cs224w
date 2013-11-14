# Call like this - awk -f transform.awk -F "|" <file>
BEGIN{
	current=0;
}
{
	if ($1 in cache == 0)
	{
		cache[$1]=current;
		current = current + 1;
	}

	if($2 in cache == 0)
	{
		cache[$2]=current
		current = current + 1;
	}

	user1=$1;
	user2=$2;
	$1=$2=""
	print cache[user1], cache[user2], $0;
}
