# Made in ChatGPT and Copilot
# Licensed under the MIT License
_radexreader_complete() {
	local cur prev opts
	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"
	opts="tail jsontail last jsonlast all jsonall erase interactive"

	case "$prev" in
		tail|jsontail|last|jsonlast|all|jsonall|erase|interactive)
			return 1 # stop
			;;
	esac

	COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
}
complete -F _radexreader_complete radexreader