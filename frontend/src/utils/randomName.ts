const adjectives = [
  'Brave', 'Clever', 'Witty', 'Swift', 'Mighty', 'Nimble', 'Bold', 'Fierce', 'Quick', 'Sly'
];

const animals = [
  'Fox', 'Hawk', 'Tiger', 'Wolf', 'Eagle', 'Lion', 'Panther', 'Falcon', 'Bear', 'Shark'
];

export function randomName() {
  const adj = adjectives[Math.floor(Math.random() * adjectives.length)];
  const animal = animals[Math.floor(Math.random() * animals.length)];
  const number = Math.floor(Math.random() * 10000);
  return `${adj}${animal}${number}`;
}
