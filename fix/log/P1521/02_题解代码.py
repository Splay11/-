for(int i=1;i<=n;i++){
            for(int j=0;j<n;j++){//模n最大为n-1
                for(int k=i;k<=m;k+=i){//k表示最后一个数为多少，它一定是i的倍数
                    dp[i][j] += dp[i-1][(j-k%n+n)%n];//若前i-1个数模n为(j-k+n)%n,那么((j-k+n)%n+k)%n=j,枚举所有情况
                    dp[i][j] %= mod;
                }
            }
        }
        for(int i=1;i<=n;i++)
        {
            for(int j=0;j<n;j++)//模n最大为n-1
            {
                for(int p=i;p<=m;p+=i)//p表示最后一个数为多少，它一定是i的倍数
                {
                    dp[i][j]=(dp[i][j]+dp[i-1][(j-p%n+n)%n])%mod;//若前i-1个数模n为(j-p+n)%n,那么((j-p+n)%n+p)%n=j,枚举所有情况
                }
            }
        }