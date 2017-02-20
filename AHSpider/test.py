import re

inputStr = "<td>409</td><td>171592.02</td>  <td>73628.4692412</td>  <!-- <td>22801.11</td> -->   <td>97963.5507588</td>"
replacedStr = re.sub(r'<!-- <td>.*?</td> -->', "dddd", inputStr);
print replacedStr; 