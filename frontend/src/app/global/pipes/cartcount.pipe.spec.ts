import { CartcountPipe } from './cartcount.pipe';

describe('CartcountPipe', () => {
  it('create an instance', () => {
    const pipe = new CartcountPipe();
    expect(pipe).toBeTruthy();
  });
});
