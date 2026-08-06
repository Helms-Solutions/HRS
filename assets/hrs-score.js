const questions=[
{cat:'Health',q:'Do you know your Medicare plan’s annual maximum out-of-pocket exposure?',a:[['Yes',10],['Somewhat',5],['No',0]]},
{cat:'Health',q:'Have your prescriptions, doctors, and preferred hospitals been reviewed in the last 12 months?',a:[['Yes',10],['Some of them',5],['No',0]]},
{cat:'Health',q:'Do you have a plan for expenses Medicare may not fully cover, such as hospital, dental, vision, hearing, or critical illness costs?',a:[['Yes',10],['Partly',5],['No',0]]},
{cat:'Retirement',q:'Do you know how much reliable monthly income you need in retirement?',a:[['Yes',10],['Rough estimate',5],['No',0]]},
{cat:'Retirement',q:'Have inflation, taxes, and market loss risk been considered in your retirement strategy?',a:[['Yes',10],['Somewhat',5],['No',0]]},
{cat:'Retirement',q:'Do you have accessible emergency funds without disrupting long-term retirement assets?',a:[['Yes',10],['Limited',5],['No',0]]},
{cat:'Security',q:'Do you have a written plan for long-term care or home health care costs?',a:[['Yes',10],['Informal plan',5],['No',0]]},
{cat:'Security',q:'Are beneficiaries, powers of attorney, final wishes, and estate documents current?',a:[['Yes',10],['Some are current',5],['No',0]]},
{cat:'Security',q:'Would your spouse or family remain financially stable after a major illness or death?',a:[['Yes',10],['Not sure',5],['No',0]]},
{cat:'Security',q:'Have all major retirement risks been reviewed together within the last year?',a:[['Yes',10],['Some areas',5],['No',0]]}
];
let step=0,answers={};
const root=document.querySelector('[data-hrs-score]');
if(root){
const qbox=root.querySelector('[data-question]'),progress=root.querySelector('[data-progress]'),back=root.querySelector('[data-back]'),next=root.querySelector('[data-next]'),result=root.querySelector('[data-result]');
function render(){const item=questions[step];progress.style.width=((step)/questions.length*100)+'%';qbox.innerHTML=`<p class="hrs-kicker">${item.cat} · Question ${step+1} of ${questions.length}</p><h3>${item.q}</h3><div class="hrs-options">${item.a.map((x,i)=>`<label><input type="radio" name="hrs-q" value="${x[1]}" ${answers[step]===x[1]?'checked':''}><span>${x[0]}</span></label>`).join('')}</div>`;back.hidden=step===0;next.textContent=step===questions.length-1?'See My HRS Score':'Next Question'}
next.addEventListener('click',()=>{const selected=qbox.querySelector('input:checked');if(!selected){alert('Please choose an answer.');return;}answers[step]=Number(selected.value);if(step<questions.length-1){step++;render();}else{finish();}});
back.addEventListener('click',()=>{if(step>0){step--;render();}});
function finish(){const total=Object.values(answers).reduce((a,b)=>a+b,0);const label=total>=80?'Strong foundation':total>=60?'Good start with gaps':total>=40?'Several areas need attention':'High-priority review recommended';progress.style.width='100%';root.querySelector('.hrs-score-card').hidden=true;result.hidden=false;result.innerHTML=`<p class="hrs-kicker">Your educational HRS Score</p><div class="hrs-result-number">${total}<small>/100</small></div><h2>${label}</h2><p>Your score highlights how well your Health, Retirement, and Security plans work together. It is not a financial, medical, legal, or insurance recommendation.</p><div><span class="hrs-pill">Health reviewed</span><span class="hrs-pill">Retirement reviewed</span><span class="hrs-pill">Security reviewed</span></div><div class="hrs-actions"><a class="hrs-btn hrs-btn-primary" href="retirement-blueprint.html">Get the Blueprint</a><a class="hrs-btn" style="background:#edf2f7;color:#172033" href="https://calendly.com/helmsretirement" target="_blank" rel="noopener">Review My Score</a></div>`;window.dispatchEvent(new CustomEvent('hrsScoreComplete',{detail:{score:total}}));}
render();}
