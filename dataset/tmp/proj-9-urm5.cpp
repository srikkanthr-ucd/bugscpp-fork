#define PJ_LIB__

#include <errno.h>
#include <math.h>

#include "proj.h"
#include "proj_internal.h"

PROJ_HEAD(urm5, "Urmaev V") "\n\tPCyl, Sph, no inv\n\tn= q= alpha=";

namespace { // anonymous namespace
struct pj_opaque {
    double m, rmn, q3, n;
};
} // anonymous namespace


static PJ_XY s_forward (PJ_LP lp, PJ *P) {           /* Spheroidal, forward */
    PJ_XY xy = {0.0, 0.0};
    struct pj_opaque *Q = static_cast<struct pj_opaque*>(P->opaque);
    double t;

    t = lp.phi = aasin (P->ctx, Q->n * sin (lp.phi));
    xy.x = Q->m * lp.lam * cos (lp.phi);
    t *= t;
    xy.y = lp.phi * (1. + t * Q->q3) * Q->rmn;
    return xy;
}


PJ *PROJECTION(urm5) {
    double alpha, t;
    struct pj_opaque *Q = static_cast<struct pj_opaque*>(pj_calloc (1, sizeof (struct pj_opaque)));
    if (nullptr==Q)
        return pj_default_destructor(P, ENOMEM);
    P->opaque = Q;

    if (pj_param(P->ctx, P->params, "tn").i) {
        Q->n = pj_param(P->ctx, P->params, "dn").f;
        if (Q->n <= 0. || Q->n > 1.)
            return pj_default_destructor(P, PJD_ERR_N_OUT_OF_RANGE);
    } else {
            return pj_default_destructor(P, PJD_ERR_N_OUT_OF_RANGE);
    }
    Q->q3 = pj_param(P->ctx, P->params, "dq").s / 3.;

    alpha = pj_param(P->ctx, P->params, "ralpha").f;
    t = Q->n * sin (alpha);
    Q->m = cos (alpha) / sqrt (1. - t * t);
    Q->rmn = 1. / (Q->m * Q->n);

    P->es = 0.;
    P->inv = nullptr;
    P->fwd = s_forward;

    return P;
}
