package main

import (
    "fmt"
    "os"
    "os/exec"
    "syscall"
)

func main() {

    usage := `usage: jpipe {jp,jpp} ...

positional arguments:
  {jp,jpp}
    jp      standard CLI for JMESPath
    jpp     jpp is an extended superset of the jp CLI for JMESPath
`

    command := ""
    if len(os.Args) > 1 {
        command = os.Args[1]
    }
    switch command {
    case "jp", "jpp":

        binary, lookErr := exec.LookPath(fmt.Sprintf("jpipe-%s", command))
        if lookErr != nil {
            panic(lookErr)
        }

        args := []string{}
        for i := 1; i < len(os.Args); i++ {
            args = append(args, os.Args[i])
        }

        env := os.Environ()

        execErr := syscall.Exec(binary, args, env)
        if execErr != nil {
            panic(execErr)
        }

    case "-h", "--help":
        fmt.Print(usage)
        os.Exit(0)
    default:
        fmt.Fprintf(os.Stderr, usage)
        os.Exit(2)
    }
}
