--[[
  bodenkraft-frontmatter-validate.lua

  Quarto Lua filter that validates the `bodenkraft:` YAML frontmatter block
  of every rendered document against the BodenKraft Document Standard.

  What this filter does:
    1. Reads the `bodenkraft:` metadata block from the document.
    2. Verifies all required fields are present.
    3. Verifies all fields use values from the controlled vocabularies.
    4. Fails the build with a clear error message if validation fails.

  What this filter does NOT do (yet — see TODO):
    - Full JSON Schema validation (needs an external Lua library or a
      sidecar Python/Node validator).
    - Cross-document reference checking (doc_id collisions, supersedes
      targets).
    - Badge <-> fact_sources consistency.
    - JSON-LD emission into rendered HTML.

  These advanced checks are performed by the separate CI workflow
  `.github/workflows/validate.yml` using ajv against
  `schema/bodenkraft-frontmatter.json`.

  License: MIT
  Part of: bodenkraft-doc-standard v1.0.0-draft
--]]

local REQUIRED_FIELDS = {
  "doc_id",
  "doc_type",
  "doc_version",
  "doc_status",
  "classification",
  "did",
}

local DOC_TYPES = {
  pdd = true,
  whitepaper = true,
  charter = true,
  contract = true,
  rulebook = true,
  manifest = true,
  pitch = true,
  standard = true,
  ["monitoring-plan"] = true,
  annex = true,
  catalog = true,
}

local DOC_STATUSES = {
  draft = true,
  review = true,
  approved = true,
  superseded = true,
  retracted = true,
}

local CLASSIFICATIONS = {
  Public = true,
  Internal = true,
  Confidential = true,
  Restricted = true,
}

local DOC_ID_PATTERN = "^BK%-[A-Z]+%-[A-Z0-9-]+%-%d%d%d$"
local DOC_VERSION_PATTERN = "^%d+%.%d+%.%d+"
local DID_PATTERN = "^did:[a-z0-9]+:"

local function meta_to_string(v)
  if v == nil then return nil end
  if type(v) == "string" then return v end
  if v.t == "MetaInlines" or v.t == "MetaBlocks" then
    return pandoc.utils.stringify(v)
  end
  if type(v) == "table" then
    return pandoc.utils.stringify(v)
  end
  return tostring(v)
end

local function fail(msg)
  io.stderr:write("\n[bodenkraft-doc-standard] VALIDATION ERROR: " .. msg .. "\n\n")
  os.exit(1)
end

function Meta(meta)
  local bk = meta.bodenkraft

  if bk == nil then
    io.stderr:write(
      "\n[bodenkraft-doc-standard] WARNING: document is missing the " ..
      "`bodenkraft:` frontmatter block. " ..
      "See BODENKRAFT_DOC_STANDARD.md §3.\n"
    )
    return nil
  end

  for _, field in ipairs(REQUIRED_FIELDS) do
    if bk[field] == nil then
      fail("required field `bodenkraft." .. field .. "` is missing.")
    end
  end

  local doc_id = meta_to_string(bk.doc_id)
  if not doc_id:match(DOC_ID_PATTERN) then
    fail("`bodenkraft.doc_id` = '" .. doc_id ..
         "' does not match pattern BK-<TYPE>-<TOPIC>-<NNN>.")
  end

  local doc_type = meta_to_string(bk.doc_type)
  if not DOC_TYPES[doc_type] then
    fail("`bodenkraft.doc_type` = '" .. doc_type ..
         "' is not a recognised value. See §5.1.")
  end

  local doc_version = meta_to_string(bk.doc_version)
  if not doc_version:match(DOC_VERSION_PATTERN) then
    fail("`bodenkraft.doc_version` = '" .. doc_version ..
         "' does not follow Semantic Versioning (e.g. 1.0.0 or 0.1.0-draft).")
  end

  local doc_status = meta_to_string(bk.doc_status)
  if not DOC_STATUSES[doc_status] then
    fail("`bodenkraft.doc_status` = '" .. doc_status ..
         "' is not a recognised lifecycle state. See §5.2.")
  end

  local classification = meta_to_string(bk.classification)
  if not CLASSIFICATIONS[classification] then
    fail("`bodenkraft.classification` = '" .. classification ..
         "' is not a recognised level. See §5.3.")
  end

  local did = meta_to_string(bk.did)
  if not did:match(DID_PATTERN) then
    fail("`bodenkraft.did` = '" .. did ..
         "' is not a valid DID (expected pattern: did:<method>:<id>).")
  end

  if doc_status == "retracted" and bk.retraction_reason == nil then
    fail("`bodenkraft.retraction_reason` is required when doc_status is 'retracted'.")
  end

  if doc_status == "superseded" and bk.superseded_by == nil then
    fail("`bodenkraft.superseded_by` is required when doc_status is 'superseded'.")
  end

  return meta
end
