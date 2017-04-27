# encoding: utf-8
"""Account data description."""

from datetime import datetime

from marrow.mongo import Document, Index  # Basic document type and index.
from marrow.mongo.field import ObjectId, String, Array, Embed, Date, Boolean  # Field types.
from marrow.mongo.document import Note  # External document type loaded by name.




class Credential(Document):
	pass


class Account(Document):
	__collection__ = 'accounts'
	__database__ = 'default'
	__pk__ = 'id'
	__reverse__ = '_account'
	
	# ## Nested Structures
	
	class Number(Document):
		__pk__ = 'number'
		
		KINDS = {
				'business',
				'personal',
				'mobile',
			}
		
		kind = String(choices=KINDS, default="business", assign=True)
		number = String()
		primary = Boolean(default=False)
	
	class Membership(Document):
		"""Organization members and roles."""
		
		# ### Field Definitions
		
		account = String()
		name = String()
		roles = Array(kind=String(default=lambda: [], assign=True))
		
		# ### Python Magic Methods
		
		def __repr__(self):
			return "Member({0.account}, {0.name!r}, roles={1})".format(self, "{" + ", ".join(sorted(self.roles)) + "}")
	
	class Setting(Document):
		source = ObjectId()
		key = String()
		value = Field()
	
	class LastContact(Document):
		when = Date()
		by = ObjectId(default=None)
	
	# ## Field Definitions
	
	id = ObjectId('_id', assign=True)  # Each user is given a unique identifier.
	state = String()  # Object state.
	
	username = String(default=None)  # Optional "short name" for authentication.
	locale = String(default='fr-CA-u-tz-cator-cu-CAD', assign=True)  # IETF BCP-47 language tag.
	name = String()  # Full name.
	
	email = Array(VerifiedMail, default=lambda: [], assign=True)  # E-mail addresses.
	credential = Array(Credential, project=False)  # Multiple credentials are permitted.
	membership = Array(Membership, default=lambda: [], assign=True)  # Organization membership.
	permission = Array(String(), default=lambda: [], assign=True)  # Abstract permission tags.
	settings = Array(Setting, default=lambda: [], assign=True)
	
	notes = Array(kind=Note, default=lambda: [], assign=True)  # Arbitrary notes.
	
	modified = Date(default=datetime.utcnow, assign=True)
	seen = Date()  # Last time seen active on site.
	contacted = Embed(kind=LastContact, default=lambda: Account.LastContact(), assign=True)
	
	# ## Indexes
	
	_username = Index('username', unique=True, sparse=True)
	_email_address = Index('email.address', unique=True)
	
	# ## Authentication Extension API Hooks
	
	@classmethod
	def lookup(cls, context, identifier):
		c = context._account_collection
		
		document = cls.from_mongo(c.find_one(cls.id == identifier))
		
		
		
				if 'active' not in result:
			return None
		
		return result
	
	@classmethod
	def authenticate(cls, context, challenge, response):
		try:
			account = cls.bind(context.db.account).find(cls.credential.match(challenge), {'credential.$': 1, 'permission': 1})[0]
		except IndexError:
			return None
		
		if 'active' not in account.permission:
			return None
		
		credential = Document.from_mongo(account.credential[0])
		if credential.valid(context, response):
			return account._id
		
		return None