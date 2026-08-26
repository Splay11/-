## 思路：哈希表模拟

使用哈希表来模拟函数的重载和调用。我们可以将函数的名字和参数类型组合作为哈希表的键，函数的返回类型作为哈希表的值。这样，我们就可以在O(1)的时间复杂度内完成函数的创建和调用。

具体的步骤如下：

1. 创建一个哈希表`mp`来存储函数的名字和参数类型组合，以及另一个哈希表`name`来存储函数的名字。

2. 对于每一个操作，首先解析输入的字符串，获取函数的名字、参数类型和返回类型。

3. 如果是创建函数的操作，首先检查`mp`中是否已经存在相同的名字和参数类型组合，如果存在，则输出"redefinition of xxx."，否则，将这个组合添加到`mp`中，并将函数的名字添加到`name`中，然后输出"Yes."。

4. 如果是调用函数的操作，首先检查`mp`中是否存在相同的名字和参数类型组合，如果存在，则输出"Yes."，否则，检查`name`中是否存在相同的名字，如果存在，则输出"xxx was not declared in this scope."，否则，输出"There is no function xxx."。

### **时间复杂度**:$O(n)$

## 代码


### python

```python
n = int(input())

mp = dict()
name = dict()

for i in range(n):
    t = int(input())
    if t == 1:
        s = input().split('(')
        pre = s[0].split()
        suf = s[1][:-1].split(',')
        str = pre[1]
        par = []
        for i in range(len(suf)):
            if suf[i] == '':
                continue
            par.append(suf[i].split()[0])
        #         par.sort()
        for i in range(len(par)):
            str += par[i]
        if mp.get(str, 0) == 0:
            mp.setdefault(str, 1)
            name.setdefault(pre[1], 1)
            print('Yes.')
        else:
            print("redefinition of "+ pre[1] + ".")
    else:
        s = input().split('(')
        par = s[1][:-1].split(',')
        str = s[0]
        for i in range(len(par)):
            if par[i] == '':
                continue
            str += par[i].split()[0]
        if mp.get(str, 0) != 0:
            print('Yes.')
        else:
            if name.get(s[0], 0) != 0:
                print(s[0] + " was not declared in this scope.")
            else:
                print("There is no function " + s[0] + ".")
```



**c++**

```cpp
#include<iostream>
#include<vector>
#include<string>
#include<unordered_map>
#include<algorithm>
using namespace std;

bool check(vector<string> v1,vector<string> v2){
    int m=v1.size(),n=v2.size();
    if(m!=n){
        return false;
    }
    for(int i=0;i<m;i++){
        if(v1[i]!=v2[i]){
            return false;
        }
    }
    //完全相同则返回true
    return true;
}

int main(){
    int q,op;
    string s;
    cin>>q;
    unordered_map<string,unordered_map<string,vector<vector<string>>>> ump;
    while(q--){
        cin>>op;
        cin.get();
        getline(cin,s);
        int pos=s.find('(');
        string s1=s.substr(0,pos),s2=s.substr(pos);//函数名，参数列表
        int l=s2.size(),pre=0;//逗号坐标
        vector<string> tmp;
        //调用
        if(s1.find(' ')==string::npos){
            for(int i=0;i<l;i++){
                if(s2[i]==','||s2[i]==')'){
                    string ss2=s2.substr(pre+1,i-pre-1);
                    tmp.push_back(ss2);
                    pre=i;
                }
            }
            if(!ump.count(s1)){
                cout<<"There is no function "<<s1<<"."<<endl;
            }
            else{
                bool flag=false;
                for(auto& p:ump[s1]){
                    for(auto& q:p.second){
                        if(check(q,tmp)){
                            flag=true;
                            cout<<"Yes."<<endl;
                            break;
                        }
                    }
                    if(flag){
                        break;
                    }
                }
                if(!flag){
                    cout<<s1<<" was not declared in this scope."<<endl;
                }
            }
        }
        //重载
        else{
            int p=s1.find(' ');
            string ss1=s1.substr(0,p),ss2=s1.substr(p+1);//返回值类型，函数名
            for(int i=0;i<l;i++){
                if(s2[i]==' '){
                    string ss2=s2.substr(pre+1,i-pre-1);
                    tmp.push_back(ss2);
                }
                else if(s2[i]==','){
                    pre=i;
                }
            }
            bool flag=false;
            if(ump.count(ss2)){
                for(auto& p:ump[ss2]){
                    for(auto& q:p.second){
                        if(check(q,tmp)){
                            flag=true;
                            cout<<"redefinition of "<<ss2<<"."<<endl;
                            break;
                        }
                    }
                    if(flag){
                        break;
                    }
                }
            }
            if(!flag){
                cout<<"Yes."<<endl;
            }
            ump[ss2][ss1].push_back(tmp);
        }
    }
    return 0;
}
```

**Java**

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(reader.readLine());
        Map<String, List<String[]>> map= new HashMap<>();
        while (q-- > 0) {
            int op = Integer.parseInt(reader.readLine());
            String s = reader.readLine();
            String[] sb = s.split("[\\s+\\,\\(\\)]");

            if (op == 1) {  // 创建
                // 如果不存在
                if (!map.containsKey(sb[1])) {
                    List<String[]> list = new ArrayList<>();
                    list.add(sb);
                    map.put(sb[1], list);
                    System.out.println("Yes.");
                } else {
                    List<String[]> list = map.get(sb[1]);
                    boolean flag = false;
                    for(String[] tmp : list) {
                        boolean flag1 = false;
                        // 某次匹配失败
                        if (tmp.length == sb.length) {
                            for (int i = 2; i < sb.length; i += 2) {
                                // 找到一个参数类型不相等
                                if (!sb[i].equals(tmp[i])) {
                                    flag1 = true;
                                    break;
                                }
                            }
                            // 找到一个参数列表完全相等的
                            if (!flag1) {
                                flag = true;
                                break;
                            }
                        }
                    }
                    if (flag) {
                        System.out.println("redefinition of " + sb[1] + ".");
                    } else {
                        System.out.println("Yes.");
                        list.add(sb);
                        map.put(sb[1], list);
                    }


                }
            } else {
                // 存在函数名
                if (map.containsKey(sb[0])) {
                    List<String[]> list = map.get(sb[0]);
                    boolean flag = false;
                    for (String[] tmp : list) {
                        boolean flag1 = false;
                        // 找到参数列表长度相同的
                        if (tmp.length == sb.length * 2) {
                            for (int i = 1; i < sb.length; i++) {
                                // 找到一个不相同的参数类型
                                if (!sb[i].equals(tmp[i * 2])) {
                                    flag1 = true;
                                    break;
                                }
                            }
                            // 找到一个参数列表相同的
                            if (!flag1) {
                                flag = true;
                                break;
                            }
                        }
                    }
                    if (flag) {
                        System.out.println("Yes.");
                    } else {
                        System.out.println(sb[0] + " was not declared in this scope.");
                    }
                } else {
                    System.out.println("There is no function " + sb[0] + ".");
                }
            }
        }
    }

}
```