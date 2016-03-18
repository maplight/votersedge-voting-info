// import 'babel/polyfill';
import { canUseDOM } from 'fbjs/lib/ExecutionEnvironment';

const VotingInfoMenu = {
  'my-polling-place': {'Major': [] , 'Minor': [
    'polling-place-address', 
    'check-polling-place'
  ]},
  'register-to-vote': {'Major': [], 'Minor': [
    'how-do-i-register-to-vote',
    'can-i-register-to-vote',
    'what-is-permanent-vote-by-mail',
    'do-i-have-to-register-again',
    'political-party',
    'what-if-i-need-language-assistance',
    'safe-at-home',
    'military-overseas',
    'college-student',
    ]},
  '
  ways-to-vote': {'Major': [
    'ways-to-vote'
      ], 'Minor': [
    'vote-by-mail',
    'get-vote-by-mail-ballot',
    'return-vote-by-mail-ballot',
    'vote-early-in-person'
    'vote-at-polling-place-in-person',
    'other-places-to-vote-in-person'
  ]},
  
  'voting-basics': {'Major': [], 'Minor': [
    'access-disabilities',
    'language-assistance',
    'voter_id',
    'correct-voting-mistake',
    'not-on-voting-rolls-at-polling-place',
    'what-is-provisional-ballot',
    'where-do-i-vote-if-i-move',
    'military-overseas',
    'safe-at-home',
    'how-to-vote-for-write-in-candidate',
    'what-is-top-two-primary',
    'what-is-ranked-choice-voting'
  ]},

  'important-dates-deadlines': {'Major': [
    'important-dates-deadlines'
      ], 'Minor': [
    'when-is-voter-registration-deadline',
    'when-is-vote-by-mail-application-deadline',
    'when-do-i-vote'
  ]},

  'my-rights-as-a-voter': {'Major': [], 'Minor': [
    'voter-bill-of-rights',
    'disability-access',
    'language-assistance',
    'safe-at-home',
    'confidentiality-and-voter-records'
  ]},

  'more-voting-info': {'Major': [], 'Minor': [
    'be-poll-worker-state',
    'be-poll-worker-county',
    'contact-league-women-voters-ca',
    'contact-league-women-voters-county',
    'glossary',
    'political-parties',
    'evaluating-ballot-measures-state',
    'evaluating-california-budget-taxes',
    'voter-registration-drives'
  ]},

  'election-office': {'Major': [], 'Minor': [
    'announcements',
    'more-information'
    'governments',
  ]},
  'election-office-contact': {'Major': [], 'Minor': [
    'contact-state-elections-office',
    'contact-county-elections-office'
  ]},
};

export default VotingInfoMenu;