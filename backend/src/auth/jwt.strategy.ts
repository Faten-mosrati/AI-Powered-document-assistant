import { Injectable, UnauthorizedException } from '@nestjs/common';
import { AuthGuard, PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { ConfigService } from '@nestjs/config';
import { UsersService } from '../users/users.service';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(
    config: ConfigService,
    private readonly usersService: UsersService,
  ) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      secretOrKey: config.getOrThrow<string>('JWT_SECRET'),
    });
  }

 async validate(payload: { sub: number }) {
  const user = await this.usersService.findById(payload.sub);
  if (!user) throw new UnauthorizedException();
  const { password, ...safeUser } = user;
  return safeUser;
}
}

@Injectable()
export class JwtGuard extends AuthGuard('jwt') {}