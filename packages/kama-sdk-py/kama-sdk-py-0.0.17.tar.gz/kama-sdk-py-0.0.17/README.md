### remind me to say:
- cached: foo in models has lower precedence than props in regular config 
- everything **MUST** be in snake case
- models are both configuration and state as they are dynamic


### Design philosophy points

The sugar in YAML. Limited because it's not a proper automaton-backed CFG, 
but aesthetically I really wanted to avoid the `.github`-style `do_this()` 
which really makes it feel like a poor-man's Turing-complete Frankenstein.


#### good example to show

```
kind: Supplier
id: foo
cached:
  res:
    kind: ResourcesSupplier
    selector:
      res_kind: Secret
      name: gcp-svc-acct-keyfile
    many: false
    serializer: native
  key_one: get::self>>res=>decoded_data->.gcp_svc_acct_keyfile
```

All providers:

## Operations & Actions

Main operations list: org.provider.operations.system


