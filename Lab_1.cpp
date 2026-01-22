#include <bits/stdc++.h>
#include <fstream>
using namespace std;

#define dup(x) cout << x << ' ' << endl;
#define ceil(a, b) ((a + b - 1) / b)
#define min3(a1, b1, cost) min(a1, min(b1, cost))
#define min4(a1, b1, cost, d) min(a1, min(b1, min(cost, d)))
#define max3(a1, b1, cost) max(a1, max(b1, cost))
#define max4(a1, b1, cost, d) max(max(a1, b1), max(cost, d))
#define ll long long
#define pb push_back
#define all(v) v.begin(), v.end()
#define veci vector<int>
#define vecd vector<double>
#define debug(a) cout << a << endl;
#define debugtwo(a1, b1) cout << a1 << ' ' << b1 << endl;
#define minvec *min_element
#define maxvec *max_element
#define zero cout << '0' << endl;
#define YES cout << "YES" << endl;
#define NO cout << "NO" << endl;
#define ub upper_bound
#define lb lower_bound
#define bs binary_search
#define minn INT_MAX
#define si set<int>
#define usi unordered_set<int>
#define vi vector<int>
#define vd vector<double>
#define umi unordered_map<int, int>
#define pii pair<int, int>
#define vpi vector<pii>
#define mii map<int, int>
#define mpi map<pii, int>
#define spi set<pii>
#define sz(x) ((int)x.size())
#define take(x) for (auto &y : x) cin >> y
#define show(x) for (auto y : x) cout << y << " "; cout << endl;
#define pq priority_queue<int>
#define pqmin priority_queue<int, vector<int>, greater<int>>
#define um unordered_map
#define mp make_pair
#define ss second
#define ff first
#define fi find
#define fbo(x) (lower_bound(all(x), val) - x.begin())
#define acc accumulate
#define rev(x) reverse(all(x))
#define sortdesc(x) sort(all(x), greater<>())
#define uniq(v) v.erase(unique(all(v)), v.end())
#define mod 1000000007
void solve()
{
    // Add your solution logic here
    int n = 5;
	// cin>>n;
	vi v = {-1, 2, -3, 4, 10};
	take(v);
	vi ans(n,0);
	int ev=0,od=1;
	for(int i =0;i<n;i++)
	{
		if(v[i]<0)
		{
			ans[od] = v[i];
			od+=2;
		}
		else
		{
			ans[ev]=v[i];
			ev+=2;
		}
	}
	show(ans);
	return;
}

int main()
{    
    ll T;
    cin >> T;
    while (T--)
    {
        solve();
    }
    return 0;
}