p = 'v8/src/execution/isolate.cc'
s = open(p).read()

# 1. 入口段: current_microtask / handler / context / extension / promise
old_e = '''void CaptureAsyncStackTrace(Isolate* isolate, CallSiteBuilder* builder) {
  Handle<Object> current_microtask = isolate->factory()->current_microtask();
  if (current_microtask->IsPromiseReactionJobTask()) {
    Handle<PromiseReactionJobTask> promise_reaction_job_task =
        Handle<PromiseReactionJobTask>::cast(current_microtask);'''
new_e = '''void CaptureAsyncStackTrace(Isolate* isolate, CallSiteBuilder* builder) {
  Handle<Object> current_microtask = isolate->factory()->current_microtask();
  PrintF("[ENTRY] microtask=%p\\n", (void*)current_microtask->ptr());
  if (current_microtask->IsPromiseReactionJobTask()) {
    Handle<PromiseReactionJobTask> promise_reaction_job_task =
        Handle<PromiseReactionJobTask>::cast(current_microtask);
    PrintF("[ENTRY] handler=%p\\n", (void*)promise_reaction_job_task->handler().ptr());'''
assert old_e in s, 'anchor-entry'
s = s.replace(old_e, new_e, 1)

old_g = '''      // Now peek into the handlers' AwaitContext to get to
      // the JSGeneratorObject for the async function.
      Handle<Context> context(
          JSFunction::cast(promise_reaction_job_task->handler()).context(),
          isolate);
      Handle<JSGeneratorObject> generator_object(
          JSGeneratorObject::cast(context->extension()), isolate);
      if (generator_object->is_executing()) {'''
new_g = '''      // Now peek into the handlers' AwaitContext to get to
      // the JSGeneratorObject for the async function.
      Handle<Context> context(
          JSFunction::cast(promise_reaction_job_task->handler()).context(),
          isolate);
      PrintF("[ENTRY-CONFUSED] handler_ctx=%p\\n", (void*)context->ptr());
      PrintF("[ENTRY-CONFUSED] ctx_extension=%p\\n", (void*)context->extension().ptr());
      Handle<JSGeneratorObject> generator_object(
          JSGeneratorObject::cast(context->extension()), isolate);
      PrintF("[ENTRY-CONFUSED] gen=%p is_executing=%d\\n", (void*)generator_object->ptr(), generator_object->is_executing() ? 1 : 0);
      if (generator_object->is_executing()) {'''
assert old_g in s, 'anchor-gen'
s = s.replace(old_g, new_g, 1)

# 2. walk 循环保留原有打印
old = '''    // Check that the {promise} is not settled.
    if (promise->status() != Promise::kPending) return;'''
new = '''    PrintF("[WALK] promise=%p\\n", (void*)promise->ptr());
    // Check that the {promise} is not settled.
    if (promise->status() != Promise::kPending) return;'''
assert old in s, 'anchor-loop'
s = s.replace(old, new, 1)

open(p, 'w').write(s)
print('isolate.cc patched (entry+loop)')
