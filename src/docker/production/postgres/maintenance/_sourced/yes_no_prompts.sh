#!/usr/bin/env bash 


yes_no(){
    declare desc="Prompt for confirmation. \$\"\{1\}\": confirmation message"
    local arg="${1}"

    local response= read -r -p "${arg} (u/[n])? " response 

    if [[ "${response}" =~ ^[Yy] ]]; then
        exit 0
    else
        exit 1
    fi
  

}