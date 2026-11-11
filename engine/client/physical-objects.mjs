// New live snapshots carry identities. Old recordings and catalogue previews
// still work by location, but an explicit identity must never fall back to a twin.
export const sameInstance=(object,reservation)=>!reservation?.instance||object?.instance===reservation.instance;
export const physicalState=(scene,item)=>item.instance?(scene.living?.instances?.[item.instance]||{}):(scene.living?.objects?.[item.id]||{});
