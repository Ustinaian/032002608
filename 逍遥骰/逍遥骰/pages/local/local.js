// pages/local/local.js
Page({
  data: {
    num:[{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0},{number:'',fl:0}],
    mdice:[''],
    dice:['','/image/1.gif?','/image/2.gif?','/image/3.gif?','/image/4.gif?','/image/5.gif?','/image/6.gif?'],
    temp:'',
    count:[0,0],
    flg:0,
    cnt:[0,0,0,0,0,0,0],
    dflag:0
  },
  setdice:function(){
    var a = Math.floor(Math.random()*6+1);
    if(this.data.dflag==0){
      this.setData({
        ['temp']:a,
        ['mdice[0]']:this.data.dice[a]+Math.random(),
        ['dflag']:1,
      })
    }
    else if(this.data.dflag==1){
    }
  },
  setdata:function(e){
    var flag = this.data.temp;
    if((this.data.flg==0 & e.currentTarget.dataset.id<=9) || (this.data.flg==1 & e.currentTarget.dataset.id>9)) return
    else if(flag=='') return
    else if(this.data.flg==0){
      this.setData({
        ['flg']:1
      })
    }
    else if(this.data.flg==1){
      this.setData({
        ['flg']:0
      })
    }
    if(e.currentTarget.dataset.id<=9){
      var i = 0;
      var t = this.data.count[0];
    }
    else{
      var i = 1;
      var t = this.data.count[1];
    }
    if(this.data.num[e.currentTarget.dataset.id].fl==0){
      this.setData({
        ['num['+e.currentTarget.dataset.id+'].number']:flag,
        ['dflag']:0,
        ['mdice[0]']:''
      })
      if(1){
        this.setData({
          ['num['+e.currentTarget.dataset.id+'].fl']:1,
          ['count['+i+']']:t+1
        })
      }
      this.set(e.currentTarget.dataset.id);
    }
    // console.log(this.data.count[0],this.data.count[1]);
    
  },
  set:function(id){
    this.setData({
      ['temp']:''
    })
    this.judge(id);
  },
  // 数字消解
  judge:function(id){
    var tmp = this.data.num[id].number;
    // console.log(id);
    if(id<=9){
      if(id<=3){
        this.clear(tmp,10,12,1)
      }
      else if(id<=6){
        this.clear(tmp,13,15,1)
      }
      else if(id<=9){
        this.clear(tmp,16,18,1)
      }
    }
    else if(id>9){
      if(id<=12){
        this.clear(tmp,1,3,0)
      }
      else if(id<=15){
        this.clear(tmp,4,6,0)
      }
      else if(id<=18){
        this.clear(tmp,7,9,0)
      }
    }
    console.log(this.data.count[0],this.data.count[1]);
    if(this.data.count[0]==9 || this.data.count[1]==9){
      this.calculate();
      wx.relaunch({
        url: '../local/end/end'
      })
    }
  },
  calculate:function(){
    this.cal(0,3,0);
    this.cal(4,6,0);
    this.cal(7,9,0);
    this.cal(10,12,1);
    this.cal(13,15,1);
    this.cal(16,18,1)
  },
  cal:function(begin,end,t){
    const app = getApp()
    for(var i=begin;i<=end;i++){
      this.data.cnt[this.data.num[i].number]++
    }
    for(var i=1;i<=6;i++){
      if(this.data.cnt[i]>0){
        app.score[t]+=this.data.cnt[i]*this.data.cnt[i]*i
        this.setData({
          ['cnt['+i+']']:0
        })
      }
    }
  },
  clear:function(tmp,begin,end,p){
    for(var i=begin;i<=end;i++){
      // console.log(tmp,this.data.num[i].number);
      if(this.data.num[i].number==tmp){
        this.setData({
          ['num['+i+'].number']:'',
          ['count['+p+']']:this.data.count[p]-1,
          ['num['+i+'].fl']:0
        })
      }
    }
  },
  onLoad:function(){
    // wx.navigateTo({
    //   url: '../local/end/end'
    // })
    getApp().score[0]=0;
    getApp().score[1]=0;
  }
})