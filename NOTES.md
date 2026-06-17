# NOTES.md

## Path chosen

_A (cache) or B (rate limiting), and why._

## If Path A (cache)

_What TTL did you choose, and why that value specifically?_

_What could a user see that is stale within that TTL window, and is that acceptable? Why?_

_What would you have to change if the weekly recommendation job started running more often?_

## If Path B (rate limiting)

_Why is per-IP the right choice for this endpoint, and not per-user?_

_What limit did you set, and what assumption about normal usage is it based on?_

_What would have to be true about this endpoint for per-user to become the better choice?_
