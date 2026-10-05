USERS 1---N IDEAS 1---N IDEA_VERSIONS 1---N EVALUATIONS
USERS 1---N HACKATHONS
Foreign keys: ideas.user_id -> users.id; idea_versions.idea_id -> ideas.id; evaluations.idea_version_id -> idea_versions.id; hackathons.user_id -> users.id.
Unique: (idea_id, version_number), users.email.
