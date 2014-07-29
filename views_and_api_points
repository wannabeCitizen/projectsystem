# Basic Views

## Home Pages

- Organization Home Page
  - Show all projects (or most recent or popular) for an organization as well as some basic info
- User Homepage
  - Show any projects or ideas user is an owner of
  - Show Ideas and projects user is *following*
  - All projects user is a *voting member* on
  - Show all pending votes user needs to address

## Pages

- Project Page (++ Create/Edit View)
- Idea Page (++ Create/Edit View and personal fork)
- Voting Page


# API Resources
Users are their own documents  
Organizations are parents of everything else (ideas, proposals, and projects are embedded documents)  
Votes are embedded documents in projects and proposals

Need to decide if we want proposal to be its own thing or whether any project with pending votes is merely treated as 
what we're calling a proposal.  It's either that or proposal is reserved for starting a project.

- User Document [Can use Google OAuth, if desired; otherwise, create own?]
  - GET [use e-mail for look up?  Or UUID?]
  - PUSH [require at least username and e-mail]
  - UPDATE
- Organization Document
  - GET Organization [look up with organization name (then must maintain uniqueness) or UUID?]
  - GET Idea [look up with organization UUID + Idea UUID]
  - GET Project [look up with organization UUID + Project UUID]
  - GET Vote [Look up with organization UUID + Project UUID + username/user UUID]
  - PUSH Organization
  - PUSH Idea
  - Push Project
  - UPDATE
