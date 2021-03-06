## 缩进:
- 每一级缩进使用四个空格，续行应该与其包裹元素对齐，要么使用圆括号、方括号和花括号内的隐式行连接来垂直对齐，要么使用挂行缩进对齐。
- 当使用挂行缩进时，应该考虑到第一行不应该有参数，以及使用缩进以区分自己是续行。

## 变量命名：
- 禁止使用字母l和O作为单字符变量名。
- 全局变量名使用圈小写。

## 每行最多字符数：
- 限制最大字符数为200。

## 函数最大行数：
- 限制函数的最大行数为50行。

## 函数、类命名：
- 模块和包名应该用简短全小写的名字。
- 类名首字母使用大写，内置的变量首字母大写命名法用于异常名或内部的常量。
- 函数名使用全小写，可以使用下划线分隔。
- 始终要将self作为实例方法的第一个参数。
- 始终要把cls作为类静态方法的第一个参数。
- 如果函数的参数名和已有的关键词冲突，则在最后加单一下划线。

## 常量：
- 常量定义在模块级，通过下划线分隔的全大写字母命名。

## 空行规则：
- 顶层函数和类的定义，前后用两个空行隔开。
- 类的方法定义用一个空行隔开。

## 注释规则：
- 注释应该是一个完整的句子。
- 在句尾结束的时候应该使用两个空格。
- 行内注释和代码至少要有两个空格分隔，注释由#和一个空格开始。
	
## 操作符前后空格：
- 逗号后面要加空格，如果后面是小括号，则不用。
- 冒号前不加空格，冒号后要加空格，但在切片里，前后都不用加空格。
- “#”后要加一个空格。
- 二元运算符前后都需要加空格，但作为函数参数时=前后不需要加空格。
- 如果使用具有不同优先级的运算符，只在具有最低优先等级的运算符周围两边添加空格，其他的就不用加了。

## 其他规则：
- 使用制表符作为缩进方式。