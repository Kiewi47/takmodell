from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
    pg=b.new_page(viewport={"width":900,"height":560});logs=[]
    pg.on("pageerror",lambda e: logs.append("ERR: "+str(e)));pg.on("console",lambda m: logs.append(m.text) if m.type=='error' else None)
    t=time.time();pg.goto("file:///mnt/user-data/outputs/takmodell.html")
    pg.wait_for_function("document.getElementById('loading').classList.contains('done')",timeout=300000);print('load s',round(time.time()-t,1))
    r=pg.evaluate("""()=>{const T=__tak;T.noIdle=true;const out=[];
      for(const h of ['en','tva','vinkel'])for(const tt of ['betong','lertegel','stilpannan','tp20']){T.setHM(h);T.setTT(tt);
        const vis=T.pick.filter(m=>{for(let q=m;q;q=q.parent)if(!q.visible)return false;return true;}).length;
        T.select('ranndal');const txt=document.getElementById('pbody').innerText.slice(0,40).replace(/\\n/g,' | ');
        out.push(h+' '+tt+' vis='+vis+' :: '+txt);T.select(null);
        const list=document.getElementById('pbody').innerText;out.push('   ränndal i listan: '+/Ränndalsplåt/.test(list)+' tätning: '+/Ränndalstätning/.test(list)+' underbeslag ränndal: '+/Underbeslag för ränndalsplåt/.test(list));}
      T.setHM('en');T.setTT('betong');return out.join('\\n');}""")
    print(r)
    print("\n".join(logs[:12]) or "inga fel");b.close()
