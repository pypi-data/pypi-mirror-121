fun arrayAppend(array1, value) {
  var l = array1.length() + 1;

  var newArray = Array(l);

  for (var i = 0; i < l - 1; i = i + 1) {
    newArray.set(i, array1.get(i));
  }

  newArray.set(l - 1, value);
  
  return newArray;
}

fun arrayConcat(array1, array2) {
  var l1 = array1.length();
  var l2 = array2.length();
  var array3 = Array(l1 + l2);

  for (var i = 0; i < array3.length(); i = i + 1) {
    if (i < l1) {
      array3.set(i, array1.get(i));
    } else {
      array3.set(i, array2.get(i - l1));
    }
  }

  return array3;
}