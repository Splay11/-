import java.util.*;

public class Main {
    static int[] parent;

    public static int find(int x){
        if(parent[x] != x){
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    public static void union(int x, int y){
        parent[find(x)] = find(y);
    }

    static class Contact{
        String name;//联系人姓名
        Set<String> phoneNum;//联系人电话
        int id;

        Contact(String name,Set<String> phoneNum,int id){
            this.name = name;
            this.phoneNum = phoneNum;
            this.id = id;
        }
    }
    //合并后
    static class MergedContact{
        String name;
        Set<String> phoneNum;

        MergedContact(String name,Set<String> phoneNum){
            this.name = name;
            this.phoneNum = phoneNum;
        }

        String getMinPhoneNumber(){
            return Collections.min(phoneNum);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        //记录数量
        int recordCount = sc.nextInt();
        sc.nextLine();
        //联系人列表
        List<Contact> contacts = new ArrayList<>();
        parent = new int[recordCount];

        //初始化并查集
        for(int i=0;i<recordCount;i++){
            parent[i] = i;
        }

        Map<String,Integer> phoneToContactId = new HashMap<>();

        for (int i = 0; i < recordCount; i++) {
            String input = sc.nextLine().trim();
            String[] tokens = input.trim().split("\\s+");
            String name = tokens[0];

            Set<String> phoneNumber = new HashSet<>();
            for (int j = 1; j < tokens.length; j++) {
                String phone = tokens[j];
                phoneNumber.add(phone);
                if (!phoneToContactId.containsKey(phone)) {
                    phoneToContactId.put(phone, i);
                } else {
                    int otherId = phoneToContactId.get(phone);
                    union(i, otherId);
                }
            }
            contacts.add(new Contact(name, phoneNumber, i));
        }
        //合并联系人
        Map<Integer,MergedContact> rootIdToMergedContact = new HashMap<>();
        for(int i=0;i<recordCount;i++){
            int root  = find(i);
            Contact contact = contacts.get(i);
            if(!rootIdToMergedContact.containsKey(root)){
                rootIdToMergedContact.put(root,new MergedContact(contact.name,new HashSet<>(contact.phoneNum)));
            }else{
                MergedContact mergedContact = rootIdToMergedContact.get(root);
                //更新姓名
                if(contact.name.compareTo(mergedContact.name) < 0){
                    mergedContact.name = contact.name;
                }
                mergedContact.phoneNum.addAll(contact.phoneNum);
            }
        }

        List<MergedContact> mergedContacts = new ArrayList<>(rootIdToMergedContact.values());
        for(MergedContact mc : mergedContacts){
            //将电话号码集改为TreeSet进行排序
            mc.phoneNum = new TreeSet<>(mc.phoneNum);
        }

        mergedContacts.sort((a,b)->{
            int nameCompare = a.name.compareTo(b.name);
            if(nameCompare!=0){
                return nameCompare;
            }else {
                String minPhoneA = a.getMinPhoneNumber();
                String minPhoneB = b.getMinPhoneNumber();
                return minPhoneA.compareTo(minPhoneB);
            }
        });

        for(MergedContact mc:mergedContacts){
           StringBuilder sb = new StringBuilder();
           sb.append(mc.name);

            List<String> sortedphones = new ArrayList<>(mc.phoneNum);
            Collections.sort(sortedphones);
            for(String phone : sortedphones){
                sb.append(" ").append(phone);
            }
            System.out.println(sb.toString());
        }
        sc.close();
    }

}
