_ntag() {
  local cur prev words cword split
  _init_completion || return
  local DEFAULTIFS=$' \t\n'
  local IFS=$DEFAULTIFS
  MAIN_CHOICE='export import add color delete filter init list make remove show path sort status add_comment get_comment filter_comment cleanup'

  case $cword in
    1)
      COMPREPLY=( $(compgen -W "$MAIN_CHOICE" -- "$cur") )
      ;;
    *)
      case ${words[1]} in
        filter | delete | add | remove)
          COMPREPLY=( $(compgen -W '$(ntag list -n)' -- "$cur") )
          ;;
        -d)
          COMPREPLY=( $(compgen -W '$(ntag list -n)' -- "$cur") )
          ;;
        esac
          ;;
  esac
}

complete -F _ntag ntag

