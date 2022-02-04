# Registers descriptions for the plugins

## Intro

In this document we will discuss all topics related to registers for the plugins.
Every plugin has group of registers that is responsible for its behavior.

# Concept

 - Every plugin has its own unique name and it should be unique. All letters should be small letters. Numbers are excepted in to the names, only in the end wof the word.

    Example: **example1**

 - Every plugin have own sub registers all sub registers is deviate by full stop "**.**"

    Example: **example.register**

 - If plugin name or sub register is constructed by more then two word the intervals between words is replaced by under score "**_**"

    Example: **example.sub_register**

 - By definition every plugin can be started or stopped. This is done through an official register. Its name is "**enabled**".

    Example: **example.enabled**

 - The Enabled register can take only two values **false** or **true**. Any other value will be interpreted as 0. The format of this register is integer.

    Example: **example.enabled = false / example.enabled = true**

 - There is few data types of registers in the system
   - Integer
   - Float
   - String
   - Array
   - JSON

    Example: 

    - example.float_register = 0.123456789
    - example.string_register = "String Value"
    - example.array_register = [1, 2, 3]
    - example.string_json = "{\"Current\": 0.327, \"ExportActiveEnergy\": 95.598, \"ApparentPower\": 80.345}"

    Note: Every register that is array can accept all data type described in this bullet.

 - In most cases every plugin contain more then one sub register. In this case, the name of the plugin is considered a namespace. So every sub register that has many is also considered as namespace.

 - The exchange format between the Zontromat and bgERP is **JSON**

 - When register exists in the system it always have allowed values. For this purpose we use few special characters to describe is this enum, interval (open and close), or just a string value.
   - In case of **Enum**, we divide possible values wit vertical pipe "**|**", example: 0|1|2|3|4|5
   - In case we have **Interval** we use slash "**/**", example: from 0 to 5, 0/5. If we wan to define a lower limit 0/. This means that all positive values are allowed. Respectively we can define upper limit by doing this /50. It means that all values below 50 are acceptable.  

# Registers

Registers description [here](registers.md)