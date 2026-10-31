p = 'v8/src/execution/isolate.cc'
s = open(p).read()

old_e = '''void CaptureAsyncStackTrace(Isolate* isolate, CallSiteBuilder* builder) {
  Handle<Object> current_microtask = isolate->factory()->current_microtask();'''
new_e = '''void CaptureAsyncStackTrace(Isolate* isolate, CallSiteBuilder* builder) {
  Handle<Object> current_microtask = isolate->factory()->current_microtask();
  PrintF("[ENTRY] microtask=%p\\n", (void*)current_microtask->ptr());'''
assert old_e in s, 'a1'
s = s.replace(old_e, new_e, 1)

old_all = '''    } else if (IsBuiltinFunction(isolate, reaction->fulfill_handler(),
                                 Builtin::kPromiseAllResolveElementClosure)) {
      Handle<JSFunction> function(JSFunction::cast(reaction->fulfill_handler()),
                                  isolate);
      Handle<Context> context(function->context(), isolate);'''
new_all = '''    } else if (IsBuiltinFunction(isolate, reaction->fulfill_handler(),
                                 Builtin::kPromiseAllResolveElementClosure)) {
      Handle<JSFunction> function(JSFunction::cast(reaction->fulfill_handler()),
                                  isolate);
      Handle<Context> context(function->context(), isolate);
      PrintF("[ALL] fulfill=%p ctx=%p ctxmap=%p slot3=%p\\n", (void*)function->ptr(), (void*)context->ptr(), (void*)context->map().ptr(), (void*)context->get(3).ptr());'''
assert old_all in s, 'a2'
s = s.replace(old_all, new_all, 1)

old_w = '''    // Check that the {promise} is not settled.
    if (promise->status() != Promise::kPending) return;'''
new_w = '''    PrintF("[WALK] promise=%p map=%p\\n", (void*)promise->ptr(), (void*)promise->map().ptr());
    // Check that the {promise} is not settled.
    if (promise->status() != Promise::kPending) return;'''
assert old_w in s, 'a3'
s = s.replace(old_w, new_w, 1)

open(p, 'w').write(s)
print('patched v2')
