"""

ASSUMPTIONS
- this tool created to bump versions, so if it can't do that it will exit with
  return code 1, meaning failure. This is so it can be used in CI/CD tooling

OVERVIEW
- [x] parse tag spec and compare with latest tag
- [x] bump the version number
- [x] write changelog
- [x] append to existing changelog file
- [x] write some tests
- [x] cli options
 - [x] dry run option
- [x] commit and tag release

- [x] more test
- [x] code coverage

- [x] version this module

- [x] ci/cd with GitHub Actions
- [x] tidy up cli arguments (sensible defaults)
- [x] create the release using github release
- other version formats
- cleanup meta data

CONSIDER
- stop commit and push if you have uncommitted changes?
- partially bump a version for the cautious people
- use the tool to detect changes, but not committing stuff?
 - git status --porcelain=v1? but portable?
- use version file to fetch version instead of tags if available?
- don't run tests if the push is coming from ci (trusted)?
- allow special switches for not doing versions for some commits (magic commands)?

UNRELATED
- generate a toc
- count loc
- test different versions of git in CI
"""

import datetime
import io
import logging
import os
import re
import subprocess
import sys


SYS_NONE = 0
SYS_WIN32 = 1
SYS_LINUX = 2
SYS_PYTHON2 = 2
SYS_PYTHON3 = 3

MIN_SUPPORTED_PYTHON_MAJOR = 3
MIN_SUPPORTED_PYTHON_MINOR = 6
MIN_SUPPORTED_PYTHON_MICRO = 0

COMMIT_PATTERN = R"^g([a-z0-9]{40}) '(.*)'"

log = logging.getLogger(__name__)


def console_entry():
 args = cli_arguments()
 release(args)


def cli_arguments():
 import argparse

 parser = argparse.ArgumentParser(prog="bumpkin", description="Standard Bumpkin", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

 parser.add_argument("--force", "-f", default=False, action="store_true", help="force a version bump if there are new commits, even if no changes were parsed")
 parser.add_argument("--debug", "-d", default=False, action="store_true")
 parser.add_argument("--dry-run", default=False, action="store_true", help="only display the commands to run")

 parser.add_argument("--preview", default=False, action="store_true", help="print a preview of the changelog to stdout")
 parser.add_argument("--no-preview", dest="preview", action="store_false")

 parser.add_argument("--push", "-p", default=True, action="store_true", help="push to repository after bumping")
 parser.add_argument("--no-push", dest="push", action="store_false")

 parser.add_argument("--tag", "-t", default=True, action="store_true", help="tag the repo with the version")
 parser.add_argument("--no-tag", dest="tag", action="store_false")

 parser.add_argument("--commit", "-c", default=True, action="store_true", help="commit changelog to history")
 parser.add_argument("--no-commit", dest="commit", action="store_false")

 parser.add_argument("--changelog-filename", "-o", default="CHANGELOG.md", metavar="FILENAME", help="filename of changelog to write changes to")
 parser.add_argument("--changelog", "-l", default=True, action="store_true", help="emit changes to changelog")
 parser.add_argument("--no-changelog", dest="changelog", action="store_false")

 parser.add_argument("--version-filename", default="VERSION", metavar="FILENAME", help="filename of version file")
 parser.add_argument("--version-file", default=True, action="store_true", help="save version string to a file")
 parser.add_argument("--no-version-file", dest="version_file", action="store_false")

 args = parser.parse_args()

 return args


def release(args):

 verbosity = 1
 use_tag = args.tag
 is_debug = args.debug
 push_tags = args.push
 is_dry_run = args.dry_run
 is_preview_changelog = args.preview
 changelog_path = args.changelog_filename
 emit_changes_to_changelog = args.changelog
 use_version_file = args.version_file
 version_file = args.version_filename
 is_committing = args.commit
 force_versioning = args.force

 DEFAULT_FORMAT = '[%(levelname)s %(asctime)s] %(message)s'
 DEBUG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

 if is_debug:
  logging.basicConfig(format=DEBUG_FORMAT)
  log.setLevel(logging.DEBUG)
  log.debug("args: %s", args)
 else:
  logging.basicConfig(format=DEFAULT_FORMAT)
  log.setLevel(logging.INFO)

 #############################
 # note/fred: context cracking

 SYS_PLATFORM = 0
 PYTHON_VERSION_MAJOR = 0
 PYTHON_VERSION_MINOR = 0

 if 0: pass
 elif sys.platform.startswith("win32"):
  SYS_PLATFORM = SYS_WIN32
 elif sys.platform.startswith("linux"):
  SYS_PLATFORM = SYS_LINUX
 else:
  log.fatal(f"sys system '{sys.platform}' is not supported")
  exit(1)

 # todo/fred: fetch which version of the platform we are using

 assert SYS_PLATFORM

 if 0: pass
 elif sys.version_info[0] == MIN_SUPPORTED_PYTHON_MAJOR:
  # todo/fred: min micro version
  if sys.version_info[1] < MIN_SUPPORTED_PYTHON_MINOR:
   log.fatal(f"python version {sys.version_info[0]}.{sys.version_info[1]} is not supported")
   exit(1)

  if sys.version_info[1] == MIN_SUPPORTED_PYTHON_MINOR and sys.version_info[2] < MIN_SUPPORTED_PYTHON_MICRO:
   log.fatal(f"python version {sys.version_info[0]}.{sys.version_info[1]} is not supported")
   exit(1)

  PYTHON_VERSION_MAJOR = SYS_PYTHON3
  PYTHON_VERSION_MINOR = sys.version_info[1]  

 else:
  log.fatal(f"python version {sys.version_info[0]}.{sys.version_info[1]} is not supported")
  exit(1)

 log.debug(f"sys.platform={sys.platform}, python.version={PYTHON_VERSION_MAJOR}.{PYTHON_VERSION_MINOR}")

 assert PYTHON_VERSION_MAJOR == MIN_SUPPORTED_PYTHON_MAJOR
 assert PYTHON_VERSION_MINOR >= MIN_SUPPORTED_PYTHON_MINOR

 if SYS_PLATFORM == SYS_WIN32:
  req_out = subprocess.run(["where", "git"], capture_output=subprocess.PIPE)
  # log.debug(f"git found at '{req_out.stdout.decode('utf-8').rstrip()}'")
  git_found = (req_out.returncode == 0)
 elif SYS_PLATFORM == SYS_LINUX:
  is_valid, which_git = cli(["which", "git"])
  git_found = is_valid
 else:
  raise NotImplementedError("os not supported yet")

 assert git_found

 if git_found == False:
  log.fatal(f"git could not be found in path")
  exit(1)

 # todo/fred: fetch which version of git we are dealing with

 #####################################
 # note/fred: github details

 is_valid, git_remote_out = cli(["git", "remote"])
 if not is_valid:
  log.fatal("could not fetch git remote")
  exit(1)

 git_remote = git_remote_out
 log.debug("using remote '%s'", git_remote)

 is_valid, git_remote_get_url_out = cli(["git", "remote", "get-url", git_remote])
 if not is_valid:
  log.fatal("could not fetch git remote url")
  exit(1)

 git_remote_url = git_remote_get_url_out
 if not git_remote_url.startswith("https://github.com"):
  log.fatal("repo '%s' doesn't seem to be a github repository", git_remote_url)
  exit(1)

 repo_url = git_remote_url
 if git_remote_url.endswith(".git"):
  assert len(repo_url) > 4
  repo_url = git_remote_url[:-4]

 assert repo_url

 if verbosity > 0:
  log.info("git repo url: %s", repo_url)

 is_valid, git_rev_parse_out = cli(["git", "rev-parse", "--abbrev-ref", "HEAD"])
 if not is_valid:
  log.fatal("could not read current branch")
  exit(1)

 git_branch = git_rev_parse_out
 assert git_branch

 log.debug("git branch: %s", git_branch)

 #
 #############################
 # note/fred: fetch latest tag

 is_first_release = False
 latest_tag = ""

 is_valid, git_describe_tags_out = cli(["git", "describe", "--tags", "--abbrev=0"])
 if not is_valid:
  log.warning("No tags were found -- treating as first release")
  is_first_release = True

  release_without_tags = True
  if not release_without_tags:
    exit(1)
 
 else:
  latest_tag = git_describe_tags_out
  log.debug("latest tag: %s", latest_tag)

 #
 ##############################
 # note/fred: parse git commits

 if is_first_release:
  git_cmd = ["git", "log", "--pretty=g%H '%s'%n%bEOC"]
 else:
  git_cmd = ["git", "log", "{}..HEAD".format(latest_tag), "--pretty=g%H '%s'%n%bEOC"]

 log.debug(" ".join(git_cmd))

 type_pattern = re.compile(R"(.*):(.*)")
 pattern = re.compile(COMMIT_PATTERN)

 is_valid, git_out = cli(git_cmd)
 if is_valid:

  string = io.StringIO(git_out)

  changes, num_commits = parse_git_commits(string, pattern, type_pattern)
  num_commits_to_report = len(changes)

  log.debug("found %d change(s) in %d commits", num_commits_to_report, num_commits)
  
  ################################
  # note/fred: fetch new version by bumping the tag according to a given tag spec

  files_to_add = []

  has_commits = (num_commits > 0)
  has_changes = (num_commits_to_report > 0)
  do_versioning_anyway = (force_versioning and has_commits)

  if has_changes or do_versioning_anyway:

   ################################
   # note/fred: aggregate changes of type

   changes_pivoted = {}
   for index, commit_hash, category, subvalue, body in changes:
    
    # @speed
    if not category in changes_pivoted:
     changes_pivoted[category] = []

    changes_pivoted[category].append((commit_hash, subvalue, body))

   log.debug(changes_pivoted)

   ################################
   # note/fred: parse tag spec

   # todo/fred: we would like to have differnt types of tag specs

   now = datetime.datetime.now()
   year = now.strftime("%Y")
   month = f"{now.month}"

   new_tag = parse_tag_spec(latest_tag, year, month, is_first_release)

   assert new_tag

   log.debug("new tag: %s", new_tag)

   ################################
   # note/fred: maintain a version file in addition to tag

   if use_version_file and not is_dry_run:
    log.debug("emitting version file: %s", version_file)
    with open(version_file, "w") as file:
     file.write(new_tag)

   if use_version_file:
    files_to_add += [version_file]

   ################################
   # note/fred: read existing changelog

   if emit_changes_to_changelog and has_changes:

    changelog_str = ""
    changelog_prev_content_str = ""
    changelog_header_str = ""

    is_changelog_existing = os.path.exists(changelog_path)

    if is_changelog_existing:

     log.debug("changelog '%s' exists, appending our changes", changelog_path)
     with open(changelog_path, "r") as existing_changelog:
      changelog_str = existing_changelog.read()

     (changelog_header_str,
      changelog_prev_content_str) = split_changelog_header_and_content(changelog_str, new_tag)

    else:
     log.debug("no changelog '%s' found, creating a new one", changelog_path)

     # note/fred: generate a new header
     with io.StringIO() as changelog_header:
      # changelog_header.write("<!--- generated: header -->")
      changelog_header.write("{}\n".format("# Changelog"))
      changelog_header.write("\n")
      changelog_header.write("All notable changes in this repository will be documented in this file.\n")
      changelog_header.write("\n")
      changelog_header.write("This format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),\n")
      changelog_header.write("and the project uses a calendar versioning scheme, 'year.month[.revision]'.\n")
      changelog_header.write("\n")
      changelog_header.write("## [Unreleased]\n")
      changelog_header.write("\n")
      changelog_header.flush()

      changelog_header.seek(0)
      changelog_header_str = changelog_header.read()

    datestr = now.strftime("%Y-%m-%d")
    changelog_content = generate_changelog_content(datestr, latest_tag, new_tag, repo_url, changes_pivoted, is_first_release)

    # todo/fred: @bug we want to maintain native line endings, is that a thing?
    # changelog_str = os.linesep.join([changelog_header_str, changelog_content, changelog_prev_content_str])
    changelog_str = "".join([changelog_header_str, changelog_content, changelog_prev_content_str])

    # todo/fred: take a backup of the existing changelog just in case until we know
    # this operation worked

    if not is_dry_run:
     with open(changelog_path, "w") as new_changelog:
      new_changelog.write(changelog_str)

    files_to_add += [changelog_path]

    if is_preview_changelog:
     print("Changelog Preview".center(80, "-"))
     print(changelog_str, end="", flush=True)
     print("-" * 80)

   else:
    if not has_changes:
     log.warning("no changes were detected in commits, skipping changelog")

   #################################
   # note/fred: commit files

   if len(files_to_add) > 0:
    git_add_cmd = ["git", "add"] + files_to_add
    git_commit_cmd = ["git", "commit", "-m", "version {}".format(new_tag)]

    if verbosity > 0:
     log.info(" ".join(git_add_cmd))
     log.info(" ".join(git_commit_cmd))

    if is_dry_run:
     pass
    elif is_committing:
     is_valid, _ = cli(git_add_cmd)
     if is_valid:
      is_valid, _ = cli(git_commit_cmd)
      if is_valid:
        pass
      else:
       log.fatal("could not commit changelog")
       exit(1)
     else:
      log.fatal("could not add changelog")
      exit(1)

   ##################################
   # note/fred: tag and push version

   branches_to_push = [new_tag]
   if emit_changes_to_changelog:
    branches_to_push += [git_branch]

   git_tag_cmd = ["git", "tag", "-a", new_tag, "-m", "version {}".format(new_tag)]
   git_push_cmd = ["git", "push", "--atomic", git_remote] + list(reversed(branches_to_push))

   if verbosity > 0:
    if use_tag:
     log.info(" ".join(git_tag_cmd))
    if push_tags:
     log.info(" ".join(git_push_cmd))

   if is_dry_run:
    pass
   else:
    if use_tag:
     is_valid, git_tag_out = cli(git_tag_cmd)
     if is_valid:

      if push_tags:
       is_valid, git_push_tags_out = cli(git_push_cmd)
       if not is_valid:
        log.fatal("could not push to remote, aborting")
        exit(1)
     
     else:
      log.fatal("could not create a tag on current commit, aborting")
      exit(1)

  else:
   log.info("no changes was parsed from the commit history, ignoring release")
   exit(1)

 else:
  log.fatal("could not run git commant '%a', aborting", git_cmd)
  exit(1)


def cli(argument_list) -> (bool, str):
 result = subprocess.run(argument_list, capture_output=subprocess.PIPE)
 return result.returncode == 0, result.stdout.decode("utf-8").strip()


def parse_git_commits(string, pattern, type_pattern):

 changes = []
 num_commits = 0
 num_commits_to_report = 0
 
 safe_words = ["https://", "http://", "ftp://"]

 while (1):

  line = string.readline()
  if line == "":
   break

  stripped_line = line.rstrip()

  if len(stripped_line) > 0 and stripped_line[0] == 'g':

   result = pattern.match(line)
   if result:
    commit_hash = result.group(1)
    subject = result.group(2)

    # log.debug("commit=%d hash=%s subject='%s'", num_commits, commit_hash, subject)

    num_commits += 1

    # note/fred: prevent urls to be parsed as types

    safe_subject = subject
    for word in safe_words:
     if word in subject:
      safe_subject = safe_subject.replace(word, "_")
      log.debug("truncating '%s' in %s", word, safe_subject)

    #######################
    # note/fred: parse type

    type_result = type_pattern.match(safe_subject)
    if type_result:
     subject_type = type_result.group(1).strip()
     subject_value = type_result.group(2).strip()
     log.debug("type: '%s', value: '%s'", subject_type, subject_value)
    else:
     # note/fred: not a type
     log.debug("subject '%s' does not contain a type -- skipping", subject)
     continue;

    assert subject_type
    assert subject_value

    # @test!
    # todo/fred: consider max number of commits supported
    MAX_COMMITS_TO_PARSE = 99999
    if num_commits > MAX_COMMITS_TO_PARSE:
     log.warning("reached a maximum number of %d commits to parse for changes, skipping the rest", num_commits)
     break

    #######################
    # note/fred: parse body

    num_lines = 0
    whole_body = ""
    while (1):
     body = string.readline().rstrip()
     num_lines += 1

     if body == "" or body == "EOC":
      break

     whole_body += body

     if num_lines > 999:
      assert False
     # todo/fred: consider max number of lines in body comment supported

    if whole_body:
     log.debug("body='%s'", whole_body)

    change = (num_commits_to_report, commit_hash, subject_type, subject_value, whole_body)
    changes.append(change)

    num_commits_to_report += 1

    # @profile
    # todo/fred: add manual gc collection if we reach ridiculous numbers of commits to parse

   else:  # if type_result:
    log.warning("commit '%s' was somehow malformed", line)
    assert False  # todo/fred: diagnose

 return changes, num_commits


def parse_tag_spec(latest_tag, year, month, is_first_release):

 current_tag = f"{year}.{month}"

 if is_first_release:
  new_tag = current_tag
 else:

  if latest_tag.startswith(current_tag):

   # note/fred: if the tags are the same, we need to bump the version
   # according to the tag spec

   tag_spec_pattern = re.compile(R"(\d{4})[.](\d{1,2})([.](\d+))?")
   tag_result = tag_spec_pattern.match(latest_tag)
   if tag_result:

    tag_groups = tag_result.groups()

    major = int(tag_groups[0])
    minor = int(tag_groups[1])
    micro = tag_groups[3]

    log.debug("parsed latest tag to major: %d, minor: %d, micro: %s", major, minor, str(micro))

    assert major
    assert minor

    if int(year) == major:
     if int(month) == minor:
      if micro:
       new_tag = "{}.{}".format(current_tag, str(int(micro) + 1))
      else:
       new_tag = "{}.{}".format(current_tag, str(1))
    else:
     # note/fred: in all other cases we restart the numbering
     new_tag = current_tag

     if int(year) > major:
      log.warning("year is from the future?")
     
     if (int(year) == major and int(month) > minor):
      log.warning("month is from the future?")

   else:
    log.warning("last tag does not match the tag spec, or unknown tag found -- setting a new tag")
    new_tag = current_tag

  else:
   log.debug("starting from zero")
   new_tag = current_tag

 return new_tag


def split_changelog_header_and_content(changelog_str, release_version) -> (str, str):

 changelog_prev_content_str = ""
 changelog_header_str = ""

 with io.StringIO(changelog_str) as existing_changelog:

  CHANGE_PATTERN = R"^<a name='(.*)'></a>"
  change_pattern = re.compile(CHANGE_PATTERN)

  line = ""
  last_pos = 0
  num_lines = 0
  is_prev_tag_found_in_changelog = False

  while 1:
   
   last_pos = existing_changelog.tell()
   line = existing_changelog.readline()

   log.debug("line %d: %s", num_lines, line.strip())
   
   if not line:
    break

   num_lines += 1

   # note/fred: this is the first occurance of an an anchor
   if line.strip().startswith("<a name='"):

    next_line = existing_changelog.readline()
    if not next_line:
     log.warning("loose hanging anchor in changelog")
     break

    line = next_line

    change_result = change_pattern.match(line)
    if change_result and change_result.group(0) == release_version:
     # todo/fred: here we can provide the option to replace or append rather than error out
     log.fatal("Version '%s' already exists in the changelog", release_version)
     exit(1)

    # @bug
    # todo/fred: this last position isn't splitting the file where we want it to

    existing_changelog.seek(last_pos)
    is_prev_tag_found_in_changelog = True

    # note/fred: the rest of it is now considered old changes
    changelog_prev_content_str = existing_changelog.read()
    break

  # todo/fred: all kinds of wierd edge cases here... could we map it out visually perhaps?

  if not is_prev_tag_found_in_changelog:
   log.warning("No previous release was found in the file, appending changes to the end of the file")
   is_force_overwrite_enabled = True
   if not is_force_overwrite_enabled:
    exit(1)

  existing_changelog.seek(0)
  # @bug?
  # note/fred: there is something odd with win32 here, maybe the newlines are strange or something?
  changelog_header_str = existing_changelog.read(last_pos)

 return changelog_header_str, changelog_prev_content_str


def generate_changelog_content(datestr, prev_version, new_version, repo_url, changes_pivoted, is_first_release) -> str:

 with io.StringIO() as changelog:

  if is_first_release:
   changelog.write("<a name='{0}'></a>\n## [{0}]".format(new_version))
  else:
   changelog.write("<a name='{0}'></a>\n## [[{0}]".format(new_version))

  # compare string
  if is_first_release:
   pass
  else:
   assert prev_version != new_version
   compare_url = "{}/compare/{}...{}".format(
    repo_url, prev_version, new_version
   )
   changelog.write("({})]".format(compare_url))

  # date
  changelog.write(" - {}\n".format(datestr))
  changelog.write("\n")

  # changes
  for category, changes in changes_pivoted.items():
   changelog.write("### {}\n".format(category.title()))
   changelog.write("\n")

   for commit_hash, change, body in changes:
    changelog.write("* {} ([{}]({}/commit/{}))\n".format(change.capitalize(), commit_hash[:7], repo_url, commit_hash))

    if body != "":
     changelog.write("{}\n".format(body))

   changelog.write("\n")

  changelog.flush()
  changelog.seek(0)
  changelog_updates_str = changelog.read()

 return changelog_updates_str
