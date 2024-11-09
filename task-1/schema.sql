Table projects {
  id integer [primary key]
  name varchar
  client_id integer
  team_id integer
  requirements text
  deadline date
}

Table employees {
  id integer [primary key]
  name varchar
}

Table teams {
  id integer [primary key]
  name varchar
  team_leader_id integer
}

Table team_members {
  id integer [primary key]
  team_id integer
  member_id integer
}

Table clients {
  id integer [primary key]
  name varchar
  email varchar
  company varchar
}

// Relationships
Ref: projects.client_id > clients.id // many-to-one
Ref: projects.team_id > teams.id // many-to-one
Ref: teams.team_leader_id > employees.id // many-to-one
Ref: team_members.team_id > teams.id // many-to-one
Ref: team_members.member_id > employees.id // many-to-one
