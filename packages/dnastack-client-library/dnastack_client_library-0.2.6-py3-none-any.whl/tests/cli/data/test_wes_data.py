TEST_WDL_FILE_CONTENTS = """version 1.0

task say_greeting {
    input {
        String name
    }

    command <<<
        echo "Hello World, my name is ~{name}!"
    >>>

    output {
        String greetings = read_string(stdout())
    }

    runtime {
        docker: "ubuntu:latest"
    }
}

workflow hello_world {
    input {
        String name
    }
    Array[Int] range = [0,1,2,3,4,5,6]
    
        call say_greeting as first_greeting {
            input: name = name
        }

    scatter (i in range){
      call say_greeting {
          input: name = name
      }
    }

    output {
        String first = first_greeting.greetings 
        Array[String] greetings = say_greeting.greetings
    }

}"""

TEST_WDL_INPUT_PARAM_CONTENTS = """{
  "hello_world.name":"Patrick"
}"""

TEST_WDL_TAG_CONTENTS = """{
  "sampleTag1":"tag1"
}"""

TEST_WDL_ENGINE_PARAM_CONTENTS = """{
  "read_from_cache":"true"
}"""
