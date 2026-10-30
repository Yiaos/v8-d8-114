p = 'v8/src/execution/isolate.cc'
s = open(p).read()
old = '''    // Check that the {promise} is not settled.
    if (promise->status() != Promise::kPending) return;'''
new = '''    PrintF("[WALK] promise=%p\\n", (void*)(*promise));
    // Check that the {promise} is not settled.
    if (promise->status() != Promise::kPending) return;'''
assert old in s, 'anchor1'
s = s.replace(old, new, 1)
old2 = '''      Handle<PromiseCapability> capability(
          PromiseCapability::cast(context->get(index)), isolate);
      if (!capability->promise().IsJSPromise()) return;
      promise = handle(JSPromise::cast(capability->promise()), isolate);
    } else if (IsBuiltinFunction(
                   isolate, reaction->fulfill_handler(),
                   Builtin::kPromiseAllSettledResolveElementClosure)) {'''
new2 = '''      Handle<PromiseCapability> capability(
          PromiseCapability::cast(context->get(index)), isolate);
      PrintF("[WALK] ALL-branch ctx=%p cap=%p promise_val=%p\\n", (void*)(*context), (void*)(*capability), (void*)(capability->promise().ptr()));
      if (!capability->promise().IsJSPromise()) { PrintF("[WALK] ALL-branch RETURN not-jspromise\\n"); return; }
      promise = handle(JSPromise::cast(capability->promise()), isolate);
    } else if (IsBuiltinFunction(
                   isolate, reaction->fulfill_handler(),
                   Builtin::kPromiseAllSettledResolveElementClosure)) {'''
assert old2 in s, 'anchor2'
s = s.replace(old2, new2, 1)
open(p, 'w').write(s)
print('isolate.cc patched')
